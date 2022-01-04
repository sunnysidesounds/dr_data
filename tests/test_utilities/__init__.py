import os
from uuid import UUID
from dr_data.utilities.file import FileUtility


def load_query(path):
    sql_file = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)), path)
    return FileUtility.read_file(sql_file)


def is_valid_uuid(uuid_to_test, version=4):
    try:
        uuid_obj = UUID(uuid_to_test, version=version)
    except ValueError:
        return False
    return str(uuid_obj) == uuid_to_test