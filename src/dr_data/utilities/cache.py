import json
from dr_data.utilities.file import FileUtility


class Cache:
    def __init__(self, config_path, cache_location='cache'):
        self.config_path = config_path
        self.configuration = json.loads(FileUtility.read_file(self.config_path))
        self.database_name = self.configuration['db']['database']
        self.cache_data = self.configuration[cache_location][self.database_name] = {}

    def append(self, key, value):
        self.cache_data[key] = value
        FileUtility.append_to_file(self.configuration, self.config_path)
