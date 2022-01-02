import pytest
import os
import psycopg2
import testing.postgresql
from dr_data.utilities.file import FileUtility


@pytest.fixture
def test_db():
    pgsql = testing.postgresql.Postgresql()
    db_conf = pgsql.dsn()
    db_con = psycopg2.connect(**db_conf)
    db_con.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    query = load_query('tests/test_sql/test_db_schema_1.sql')
    db_con.cursor().execute(query)
    yield db_con.cursor()


def load_query(path):
    sql_file = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)), path)
    return FileUtility.read_file(sql_file)


def test_db_connection(test_db):
    assert test_db is not None


def test_db_table_count(test_db):
    query = load_query('tests/test_sql/get_all_tables.sql')
    test_db.execute(query)
    tables = test_db.fetchall()
    assert len(tables) == 9
