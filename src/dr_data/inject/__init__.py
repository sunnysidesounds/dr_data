import sys
import uuid
import psycopg2.extras as psql_extras
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import pandas as pd
import psycopg2
import logging
from progress.bar import Bar
from dr_data.static_strings import *
from dr_data.randoms import Randoms
from dr_data.sql import Sql

__author__ = AUTHOR
__copyright__ = COPYRIGHT
__license__ = LICENSE

_logger = logging.getLogger(__name__)
logging.basicConfig(format='%(message)s', stream=sys.stdout, level=logging.INFO)


class Inject:
    def __init__(self, schema, configuration):
        self.configuration = configuration
        conn_info = self.configuration['db']
        self.connection = psycopg2.connect(**conn_info)
        self.database = conn_info['database']
        self.cursor = self.connection.cursor()
        self.analyzed_schema = schema

    def execute_cmd(self, how_many):
        for key, value in self.analyzed_schema.items():
            table = list(value.keys())[0]
            self.populate_table(how_many, table, value[table]['columns'])

    def build_dataframe(self, columns):
        dataframe = {}
        for column in columns:
            value = self.set_data_by_type(column)
            dataframe[column['name']] = [value]
        return pd.DataFrame(dataframe)

    def set_data_by_type(self, column):
        value = None
        # check if is_nullable is True (if False we need a value)
        if not column['is_nullable']:
            if 'constraint' in column:
                constraint_list = list(column['constraint'])
                constraint_values = list(column['constraint'].values())
                types = [const_dict['type'] for const_dict in constraint_values]
                if 'FOREIGN KEY' in types:
                    index = types.index('FOREIGN KEY')
                    constraint_name = constraint_list[index]
                    constraint = column['constraint'][constraint_name]
                    constraint_table = constraint['referenced_table']
                    constraint_column = constraint['referenced_column']
                    value = str(self.get_random_row(constraint_column, constraint_table)[0])
                elif 'PRIMARY KEY' in types and column['data_type'] == 'uuid':
                    value = str(uuid.uuid4())
                elif 'PRIMARY KEY' in types:
                    value = Randoms.get_hash(25)
                else:
                    raise Exception(INJECT_NEED_TO_IMPLEMENT_TYPE.format(types=types))

            else:
                if column['data_type'] == 'character varying':
                    value = Randoms.get_custom_text(column['name'])
                elif column['data_type'] == 'timestamp without time zone':
                    value = Randoms.get_datetime(min_year=2000)
                elif column['data_type'] == 'timestamp with time zone':
                    value = Randoms.get_datetime_with_timezone(min_year=2000)
                elif column['data_type'] == 'text':
                    value = Randoms.get_custom_text(column['name'])
                elif column['data_type'] == 'boolean':
                    value = Randoms.get_boolean()
                elif column['data_type'] == 'USER-DEFINED':
                    user_defined_values = column['user_defined_type']['values']
                    value = Randoms.get_value_from_list(user_defined_values)
                elif column['data_type'] == 'integer':
                    value = Randoms.get_number()
                else:
                    raise Exception(INJECT_NEED_TO_IMPLEMENT_TYPE.format(types=column['data_type']))

        return value

    def populate_table(self, how_many, table_name, columns_data):
        progress_bar = Bar(' - building [{}] table '.format(table_name), max=how_many)
        for index in range(how_many):
            dataframe = self.build_dataframe(columns_data)
            columns = ', '.join(dataframe.columns.tolist())
            query = Sql.build_populate_insert().format(table_name=table_name, columns=columns)
            self.insert_table_data(index + 1, query, self.connection, self.cursor, dataframe, how_many)
            progress_bar.next()
        progress_bar.finish()

    def insert_table_data(
            self,
            index: int,
            query: str,
            conn: psycopg2.extensions.connection,
            cur: psycopg2.extensions.cursor,
            df: pd.DataFrame,
            page_size: int
    ) -> None:
        data_tuples = [tuple(row.to_numpy()) for index, row in df.iterrows()]

        try:
            psql_extras.execute_values(cur, query, data_tuples, page_size=page_size)
        except Exception as error:
            logging.info("- {index}) FAILED query execution for:: \"{query}\" ".format(index=index, query=cur.query.decode("utf-8")))
            logging.info("\n")
            logging.info("ERROR: {error}".format(error=error))
            conn.rollback()
            cur.close()
            sys.exit()
        else:
            conn.commit()

    def get_random_row(self, columns, table):
        self.cursor.execute(Sql.build_random_row().format(columns=columns, table=table))
        return self.cursor.fetchone()

    def get_random_row_where(self, columns, table, query):
        self.cursor.execute(Sql.build_random_row_where().format(columns=columns, table=table, query=query))
        return self.cursor.fetchone()