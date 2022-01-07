import logging
import sys
import psycopg2
from dr_data.static_strings import *

__author__ = AUTHOR
__copyright__ = COPYRIGHT
__license__ = LICENSE

_logger = logging.getLogger(__name__)
logging.basicConfig(format='%(message)s', stream=sys.stdout, level=logging.INFO)


class DatabaseUtility:

    def __init__(self, conn_info):
        self.connection = psycopg2.connect(**conn_info)
        self.database = conn_info['database']
        self.cursor = self.connection.cursor()

    def truncate_db(self):
        try:
            self.cursor.execute("""
            CREATE OR REPLACE FUNCTION truncate_tables(username IN VARCHAR) RETURNS void AS $$
            DECLARE
                statements CURSOR FOR
                    SELECT tablename FROM pg_tables
                    WHERE tableowner = username AND schemaname = 'public';
            BEGIN
                FOR stmt IN statements LOOP
                    EXECUTE 'TRUNCATE TABLE ' || quote_ident(stmt.tablename) || ' CASCADE;';
                END LOOP;
            END;
            $$ LANGUAGE plpgsql;""")
            self.cursor.execute("""SELECT truncate_tables('postgres');""")
        except Exception as error:
            logging.info("- FAILED truncating db ")
            logging.info("\n")
            logging.info("ERROR: {error}".format(error=error))
            self.connection.rollback()
            self.cursor.close()
            sys.exit()
        else:
            self.connection.commit()