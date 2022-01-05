from dr_data.biopsy import Biopsy
from dr_data.transplant import Transplant
from test_utilities import load_file, load_query


def test_transplant_execute_cmd(test_db):
    db_conf = {
        "db": test_db['config']
    }
    transplant = Transplant(db_conf)
    table_name = 'controlled_vocabularies'
    csv_file = load_file('test_csv/transplant_test.csv')
    transplant.execute_file_cmd(csv_file, table_name)

    query = load_query('test_sql/select_all_transplants.sql')
    test_db['cursor'].execute(query)
    records = test_db['cursor'].fetchall()

    assert records[0][1] == 'transplant-test-1'
    assert records[1][1] == 'transplant-test-2'
    assert records[2][1] == 'transplant-test-3'
    assert records[3][1] == 'transplant-test-4'
    assert records[4][1] == 'transplant-test-5'
    assert records[5][1] == 'transplant-test-6'
    assert records[6][1] == 'transplant-test-7'
    assert records[7][1] == 'transplant-test-8'
    assert records[8][1] == 'transplant-test-9'
