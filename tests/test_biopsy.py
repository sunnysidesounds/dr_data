from dr_data.biopsy import Biopsy

expected_insertion_order_list = [
    '__EFMigrationsHistory',
    'controlled_vocabularies',
    'foobar_data_accounts',
    'foobar_data_instances',
    'foobar_datas',
    'storage_storage_use',
    'storages',
    'submissions',
    'tag',
    '@database_metadata'
]


def test_biopsy_execute_cmd(test_db):
    db_conf = {
        "db": test_db['config']
    }
    schema_data = Biopsy(db_conf).execute_cmd()
    insertion_order = schema_data[0]
    assert len(insertion_order) == 10
    assert type(insertion_order) is dict
    assert list(insertion_order.keys()) == expected_insertion_order_list
    schema = schema_data[1]
    assert type(schema) is dict
    assert len(schema) == 9


def test_biopsy_build_schema(test_db):
    db_conf = {
        "db": test_db['config']
    }
    schema = Biopsy(db_conf).build_schema()
    assert len(schema) == 10
    assert type(schema) is dict


def test_biopsy_build_insertion_order_schema(test_db):
    db_conf = {
        "db": test_db['config']
    }
    b = Biopsy(db_conf)
    schema = b.build_insertion_order_schema()
    assert len(schema) == 9
    assert type(schema) is dict


def test_biopsy_get_insertion_table_order(test_db):
    db_conf = {
        "db": test_db['config']
    }
    raw_db_expected_insertion_order = ['"__EFMigrationsHistory"', 'controlled_vocabularies', 'foobar_data_accounts', 'storages', 'submissions', 'foobar_datas', 'storage_storage_use', 'foobar_data_instances', 'tag']
    b = Biopsy(db_conf)
    raw_insertion_order = b.get_insertion_table_order()
    assert raw_insertion_order == raw_db_expected_insertion_order


def test_biopsy_build_tables(test_db):
    db_conf = {
        "db": test_db['config']
    }
    expected_db_tables = ['__EFMigrationsHistory', 'controlled_vocabularies', 'foobar_data_accounts', 'foobar_data_instances', 'foobar_datas', 'storage_storage_use', 'storages', 'submissions', 'tag']
    b = Biopsy(db_conf)
    tables = b.build_tables()
    assert tables == expected_db_tables


def test_biopsy_build_columns(test_db):
    db_conf = {
        "db": test_db['config']
    }
    expected_columns_data = {'columns': [{'name': 'id', 'data_type': 'uuid', 'column_default': None, 'is_nullable': False, 'constraint': {'pk_tag': {'type': 'PRIMARY KEY', 'referenced_table': 'tag', 'referenced_column': 'id'}}}, {'name': 'value', 'data_type': 'text', 'column_default': None, 'is_nullable': False}, {'name': 'foobar_data_id', 'data_type': 'uuid', 'column_default': None, 'is_nullable': False, 'constraint': {'fk_tag_foobar_datas_foobar_data_id': {'type': 'FOREIGN KEY', 'referenced_table': 'foobar_datas', 'referenced_column': 'id'}}}, {'name': 'created_by', 'data_type': 'text', 'column_default': None, 'is_nullable': False}, {'name': 'created_at', 'data_type': 'timestamp with time zone', 'column_default': None, 'is_nullable': False}, {'name': 'updated_by', 'data_type': 'text', 'column_default': None, 'is_nullable': True}, {'name': 'updated_at', 'data_type': 'timestamp with time zone', 'column_default': None, 'is_nullable': True}], '@table_metadata': {'column_count': 7, 'has_foreign_keys': True, 'has_user_defined_keys': False, 'foreign_constraint_tables': ['foobar_datas']}}
    b = Biopsy(db_conf)
    columns = b.build_columns('tag')
    assert columns == expected_columns_data


def test_biopsy_get_column_constraint(test_db):
    db_conf = {
        "db": test_db['config']
    }
    expected_constraint_data = {'fk_submissions_foobar_data_accounts_account_id': {'type': 'FOREIGN KEY', 'referenced_table': 'foobar_data_accounts', 'referenced_column': 'id'}}
    b = Biopsy(db_conf)
    constraints = b.get_column_constraint('submissions', 'account_id')
    assert constraints == expected_constraint_data


def test_biopsy_get_values_from_type(test_db):
    db_conf = {
        "db": test_db['config']
    }
    expected_types_data = ['pending_review', 'published', 'retracted', 'qc_failed', 'qc_passed']
    b = Biopsy(db_conf)
    types = b.get_values_from_type('foobar_data_status')
    assert types == expected_types_data
