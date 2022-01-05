import sys
import logging
import psycopg2
from progress.bar import Bar
from dr_data.static_strings import *
from dr_data.utilities.file import FileUtility

__author__ = AUTHOR
__copyright__ = COPYRIGHT
__license__ = LICENSE

_logger = logging.getLogger(__name__)
logging.basicConfig(format='%(message)s', stream=sys.stdout, level=logging.INFO)


class Transplant:
    def __init__(self, configuration):
        self.configuration = configuration
        conn_info = self.configuration['db']
        self.connection = psycopg2.connect(**conn_info)
        self.database = conn_info['database']
        self.cursor = self.connection.cursor()

    def execute_file_cmd(self, source, destination):
        with open(source, 'r') as csv_file:
            copy_sql = """COPY "{table_name}" FROM stdin WITH CSV HEADER DELIMITER as ','""".format(table_name=destination)
            try:
                self.cursor.copy_expert(sql=copy_sql, file=csv_file)
                self.connection.commit()
            except Exception as error:
                logging.info("- FAILED query execution for:: \"{query}\" ".format(query=self.cursor.query.decode("utf-8")))
                logging.info("\n")
                logging.info("ERROR: {error}".format(error=error))
                self.connection.rollback()
                self.cursor.close()
                sys.exit()

    def execute_directory_cmd(self, source, schema_data):
        files = FileUtility.get_directory_files(source)
        insertion_order_schema = schema_data[1]
        skipped_tables = []
        progress_bar = Bar('- Importing CSVs to {database}...'.format(database=self.database), max=len(insertion_order_schema.items()))
        for key, value in insertion_order_schema.items():
            key = list(value.keys())[0]
            if key not in files:
                skipped_tables.append(key)
                continue
            source = files[key]
            self.execute_file_cmd(source, key)
            progress_bar.next()
        progress_bar.finish()
        logging.info('- Skipped tables {tables}'.format(tables=skipped_tables))