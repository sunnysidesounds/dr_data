import os
from dr_data.utilities.file import FileUtility


def load_query(path):
    sql_file = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)), path)
    return FileUtility.read_file(sql_file)