from dr_data.biopsy import Biopsy


def test_biopsy_execute_cmd(test_db):
    db_conf = {
        "db": test_db['config']
    }
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
    schema_data = Biopsy(db_conf).execute_cmd()
    insertion_order = schema_data[0]
    assert len(insertion_order) == 10
    insertion_order_list = list(insertion_order.keys())
    assert insertion_order_list == expected_insertion_order_list
    schema = schema_data[1]
    assert len(schema) == 9
