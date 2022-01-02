import pytest
from test_utilities import load_query


def test_db_connection(test_db):
    assert test_db is not None


def test_db_table_count(test_db):
    query = load_query('test_sql/get_all_tables.sql')
    test_db.execute(query)
    tables = test_db.fetchall()
    assert len(tables) == 9
