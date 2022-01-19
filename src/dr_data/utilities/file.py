import logging
import json
import string
import csv
import os
import time
from dr_data.static_strings import *

__author__ = AUTHOR
__copyright__ = COPYRIGHT
__license__ = LICENSE

_logger = logging.getLogger(__name__)
logging.basicConfig(format='%(message)s', stream=sys.stdout, level=logging.INFO)


class FileUtility:
    """
    File utility class
    """
    @staticmethod
    def read_file(file_path):
        """
        Reads a file's contents
        :param file_path: Path of the file
        :type file_path: str
        :return: Content of file
        :rtype: str
        """
        file = open(file_path)
        contents = file.read()
        file.close()
        return contents

    @staticmethod
    def append_to_file(json_data, filename):
        """
        This append JSON data to a file
        :param json_data: JSON data to append
        :type json_data: JSON
        :param filename: Name of the file
        :type filename: str
        :return: None
        :rtype: None
        """
        with open(filename, 'w') as json_file:
            json.dump(json_data, json_file, indent=4, separators=(',', ': '))

    @staticmethod
    def get_filename(name):
        """
        Get the name of the file with date
        :param name: Name of file
        :type name: str
        :return: String of filename
        :rtype: str
        """
        file_date = time.strftime("%Y%m%d")
        return "{database}_{date}".format(database=name, date=file_date)

    @staticmethod
    def generate_json_file(name, path, data):
        """
        Generates a JSON file
        :param name: name of file to create
        :type name: str
        :param path: Path of the file to create
        :type path: str
        :param data: The JSON data to insert into the file
        :type data: JSON
        :return: Filename
        :rtype: str
        """
        file_name = FileUtility.get_filename(name)
        json_schema = json.dumps(data, indent=4)
        with open('{path}/{file_name}.json'.format(path=path, file_name=file_name),
                  'w') as outfile:
            outfile.write(json_schema)
        return file_name

    @staticmethod
    def is_csv_file(selected_file):
        """
        Check if a file is a CSV file
        :param selected_file: Path of the file to check
        :type selected_file: str
        :return: Boolean
        :rtype: bool
        """
        try:
            with open(selected_file, newline='') as csv_file:
                start = csv_file.read(4096)
                if not all([c in string.printable or c.isprintable() for c in start]):
                    return False
                dialect = csv.Sniffer().sniff(start)
                return True
        except csv.Error:
            return False

    @staticmethod
    def get_directory_files(directory):
        """
        Get the files in a directory
        :param directory: Path of the directory
        :type directory: str
        :return: Dictionary of files
        :rtype: dict
        """
        directory_files = dict()
        for root, dirs, files in os.walk(os.path.abspath(directory)):
            for file in files:
                key = os.path.splitext(file)[0]
                path = os.path.join(root, file)
                directory_files[key] = path
        return directory_files
