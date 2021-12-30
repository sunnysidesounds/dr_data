AUTHOR = 'Jason R Alexander'
COPYRIGHT = 'Jason R Alexander'
LICENSE = 'MIT'

ENV_CONFIG_NAME = 'DRDATA_CONFIG'
MAIN_DESCRIPTION = 'Utility tool that populates random or CSV data to your database for development purposes'

NO_CONFIG_ARGUMENT = 'command requires `-config` argument or set {env_name}=<path/to/file> env variable'
NO_CONFIG_FILE = '`-config={path}` does not exist.'
NO_ARGUMENTS = 'Please choose a command argument (transplant, inject, biopsy, cleanse)'

TRANSPLANT_NO_SOURCE = '`--transplant` command requires `-source` argument.'

CLEANSE_COMPLETE_MESSAGE = 'Completed cleanse for {database} database!'

BIOPSY_NO_EXPORT = '`--biopsy` command requires `-export` argument.'
BIOPSY_EXPORT_NOT_EXIST = 'Path {path} does not exist.'

BIOPSY_START_MESSAGE = 'Starting biopsy command for {database} database!'
BIOPSY_COMPLETE_MESSAGE = 'Completed biopsy for {database} database! Exported file located {export_path}'
BIOPSY_GENERATED_SCHEMA = '- Created {filename}.json schema file.'
BIOPSY_GENERATED_INSERT_ORDER_SCHEMA = '- Generated {filename}.json insertion order schema file.'