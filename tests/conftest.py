"""
    Dummy conftest.py for dr_data.

    If you don't know what this is for, just leave it empty.
    Read more about conftest.py under:
    - https://docs.pytest.org/en/stable/fixture.html
    - https://docs.pytest.org/en/stable/writing_plugins.html
"""
import pytest
import psycopg2
import testing.postgresql
from test_utilities import load_query


@pytest.fixture
def test_db():
    pgsql = testing.postgresql.Postgresql()
    db_conf = pgsql.dsn()
    db_con = psycopg2.connect(**db_conf)
    db_con.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    query = load_query('test_sql/test_db_schema_1.sql')
    db_con.cursor().execute(query)
    yield {
        "cursor": db_con.cursor(),
        "connection": db_con,
        "config": db_conf
    }