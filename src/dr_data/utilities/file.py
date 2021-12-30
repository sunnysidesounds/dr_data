import logging
import json
import os
from os.path import exists
import time
import shutil
from dr_data.config import *

from dr_data import __version__

__author__ = AUTHOR
__copyright__ = COPYRIGHT
__license__ = LICENSE

_logger = logging.getLogger(__name__)


class FileUtility:
    @staticmethod
    def read_file(file_path):
        file = open(file_path)
        contents = file.read()
        file.close()
        return contents

    @staticmethod
    def append_to_file(json_data, filename):
        with open(filename, 'w') as json_file:
            json.dump(json_data, json_file,indent=4,separators=(',',': '))

    @staticmethod
    def get_filename(name):
        file_date = time.strftime("%Y%m%d")
        return "{database}_{date}".format(database=name, date=file_date)

    @staticmethod
    def generate_json_file(name, path, data):
        file_name = FileUtility.get_filename(name)
        json_schema = json.dumps(data, indent=4)
        with open('{path}/{file_name}.json'.format(path=path, file_name=file_name),
                  'w') as outfile:
            outfile.write(json_schema)
        return file_name
