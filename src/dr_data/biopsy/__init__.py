import psycopg2
import logging
from progress.bar import Bar
from dr_data.static_strings import *
from dr_data.sql import Sql

__author__ = AUTHOR
__copyright__ = COPYRIGHT
__license__ = LICENSE

_logger = logging.getLogger(__name__)


class Biopsy:
    def __init__(self, configuration):
        self.configuration = configuration
        conn_info = self.configuration['db']

        self.connection = psycopg2.connect(**conn_info)
        self.database = conn_info['database']
        self.cursor = self.connection.cursor()
        self.schema = dict()
        self.insertion_order = dict()
        self.table_count = 0
        self.insert_order = 1

    def execute_cmd(self):
        return (
            self.build_schema(),
            self.build_insertion_order_schema()
        )

    def build_schema(self, table_schema_name='public'):
        tables = self.build_tables(table_schema_name)
        no_foreign_keys = []
        has_foreign_keys = []
        progress_bar = Bar('- Generating schema for {database}...'.format(database=self.database), max=len(tables))
        for table in tables:
            columns = self.build_columns(table)
            self.schema[table] = columns
            if columns['@table_metadata']['has_foreign_keys']:
                has_foreign_keys.append(table)
            else:
                no_foreign_keys.append(table)
            progress_bar.next()
        progress_bar.finish()
        self.schema["@database_metadata"] = {
            "no_foreign_key_tables": no_foreign_keys,
            "foreign_key_tables": has_foreign_keys
        }
        return self.schema

    def build_insertion_order_schema(self):
        if len(self.schema) == 0:
            self.build_schema()
        insertion_table_order = self.get_insertion_table_order()
        progress_bar = Bar('- Generating insertion order for {database}....'.format(database=self.database),
                           max=len(insertion_table_order))
        for table in insertion_table_order:
            table = table.replace("\"", "")
            self.insertion_order[self.insert_order] = {
                table: self.schema[table]
            }
            self.insert_order += 1
            progress_bar.next()
        progress_bar.finish()
        return self.insertion_order

    def get_insertion_table_order(self):
        query = Sql.build_insertion_table_order()
        self.cursor.execute(query)
        insertion_data = self.cursor.fetchall()
        output = []
        for insertion_name in insertion_data:
            output.append(insertion_name[0])
        return output

    def build_tables(self, table_schema_name='public'):
        query = Sql.build_tables_query().format(name=table_schema_name)
        self.cursor.execute(query)
        table_data = self.cursor.fetchall()
        data = []
        for table in table_data:
            data.append(table[1])
            self.table_count += 1
        return data

    def build_columns(self, table_name, table_schema_name='public'):
        query = Sql.build_columns_query().format(schema_name=table_schema_name, table_name=table_name)
        self.cursor.execute(query)
        column_data = self.cursor.fetchall()
        column_data_list = []

        foreign_key_tables = []
        has_foreign_keys = False
        has_user_defined_keys = False
        for column in column_data:
            constraint = self.get_column_constraint(table_name, column[2])
            insert_object = {
                "name": column[2],
                "data_type": column[5],
                "column_default": column[3],
                "is_nullable": column[4],
            }

            if column[5] == 'USER-DEFINED':
                has_user_defined_keys = True
                insert_object["user_defined_type"] = {
                    "name": column[6],
                    "values": self.get_values_from_type(column[6])
                }

            if constraint:
                insert_object["constraint"] = constraint

                for key, value in constraint.items():
                    if value['type'] == 'FOREIGN KEY':
                        foreign_key_tables.append(value['referenced_table'])
                        has_foreign_keys = True
            column_data_list.append(insert_object)

        output = {
            "columns": column_data_list,
            "@table_metadata": {
                "column_count": len(column_data),
                "has_foreign_keys": has_foreign_keys,
                "has_user_defined_keys": has_user_defined_keys,
                "foreign_constraint_tables": foreign_key_tables
            }
        }
        return output

    def get_column_constraint(self, table_name, column_name, table_schema_name='public'):
        query = Sql.build_column_constraints().format(schema_name=table_schema_name, table_name=table_name, column_name=column_name)
        self.cursor.execute(query)
        constraint_data = self.cursor.fetchall()
        data = dict()

        for constraint in constraint_data:
            data[constraint[4]] = {
                "type": constraint[5],
                "referenced_table": constraint[8],
                "referenced_column": constraint[9]
            }
        return data

    def get_values_from_type(self, type):
        query = Sql.build_values_from_type().format(type=type)
        self.cursor.execute(query)
        types = []
        type_data = self.cursor.fetchall()
        for tdata in type_data:
            types.append(tdata[1])
        return types