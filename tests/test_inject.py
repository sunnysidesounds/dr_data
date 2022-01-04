from dr_data.biopsy import Biopsy
from dr_data.inject import Inject
import datetime
from test_utilities import load_query, is_valid_uuid

column_data = [{'name': 'id', 'data_type': 'uuid', 'column_default': None, 'is_nullable': False,
                'constraint': {'pk_controlled_vocabularies': {'type': 'PRIMARY KEY',
                                                              'referenced_table': 'controlled_vocabularies',
                                                              'referenced_column': 'id'}}},
               {'name': 'name', 'data_type': 'text', 'column_default': None, 'is_nullable': False},
               {'name': 'discriminator', 'data_type': 'text', 'column_default': None, 'is_nullable': False},
               {'name': 'created_by', 'data_type': 'text', 'column_default': None, 'is_nullable': False},
               {'name': 'created_at', 'data_type': 'timestamp with time zone', 'column_default': None,
                'is_nullable': False},
               {'name': 'updated_by', 'data_type': 'text', 'column_default': None, 'is_nullable': True},
               {'name': 'updated_at', 'data_type': 'timestamp with time zone', 'column_default': None,
                'is_nullable': True}
               ]


def test_inject_execute_cmd(test_db):
    db_conf = {
        "db": test_db['config']
    }
    rows = 2
    schema_data = Biopsy(db_conf).execute_cmd()
    Inject(schema_data[1], db_conf).execute_cmd(rows)

    query = load_query('test_sql/get_table_row_counts.sql')
    test_db['cursor'].execute(query)
    tables = test_db['cursor'].fetchall()
    for table in tables:
        assert table[1] == rows


def test_inject_set_data_by_type(test_db):
    db_conf = {
        "db": test_db['config']
    }
    schema_data = Biopsy(db_conf).execute_cmd()
    injected = Inject(schema_data[1], db_conf)

    column1 = injected.set_data_by_type(column_data[0])
    column2 = injected.set_data_by_type(column_data[1])
    column3 = injected.set_data_by_type(column_data[2])
    column4 = injected.set_data_by_type(column_data[3])
    column5 = injected.set_data_by_type(column_data[4])
    column6 = injected.set_data_by_type(column_data[5])
    column7 = injected.set_data_by_type(column_data[6])
    assert is_valid_uuid(column1)
    assert type(column2) is str
    assert type(column3) is str
    assert type(column4) is str
    assert type(column5) is datetime.datetime
    assert column6 is None
    assert column7 is None


def test_inject_populate_table(test_db):
    db_conf = {
        "db": test_db['config']
    }
    table_name = 'controlled_vocabularies'
    how_many = 2
    schema_data = Biopsy(db_conf).execute_cmd()
    injected = Inject(schema_data[1], db_conf).populate_table(how_many, table_name, column_data)
    assert injected is None


def test_inject_get_random_row(test_db):
    db_conf = {
        "db": test_db['config']
    }
    table_name = 'controlled_vocabularies'
    how_many = 10
    schema_data = Biopsy(db_conf).execute_cmd()
    injected = Inject(schema_data[1], db_conf)
    injected.populate_table(how_many, table_name, column_data)
    results = injected.get_random_row('name', 'controlled_vocabularies')
    assert results is not None


def test_inject_get_random_row_where(test_db):
    db_conf = {
        "db": test_db['config']
    }
    table_name = 'controlled_vocabularies'
    how_many = 10
    schema_data = Biopsy(db_conf).execute_cmd()
    injected = Inject(schema_data[1], db_conf)
    injected.populate_table(how_many, table_name, column_data)
    results = injected.get_random_row_where('name', 'controlled_vocabularies', 'WHERE updated_by is NULL')
    assert results is not None