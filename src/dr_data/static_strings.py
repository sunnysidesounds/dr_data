# Licensing
AUTHOR = 'Jason R Alexander'
COPYRIGHT = 'Jason R Alexander'
LICENSE = 'MIT'

# Argument messages
TRANSPLANT_ARG = 'Insert one or all CSV files to table'
TRANSPLANT_SOURCE_ARG = 'Used in conjuctions with `transplant` The CSV source file or directory. if directory, csv filenames need to match table names '
TRANSPLANT_DESTINATION_ARG = 'Used in conjuctions with `transplant` and `source`. if `source` is a file. destination TABLE is required'
INJECT_ARG = 'Inserts one or many randomly regenerated rows'
INJECT_ROW_ARG = 'How may rows do you want to load per table in the database, default is set in configuration'
BIOPSY_ARG = 'Explicitly exports a schema and table insertion-order JSON files'
BIOPSY_EXPORT_ARG = 'The directory PATH to export the JSON files'
CLEANSE_ARG = 'Truncates all the values in the database'
CONFIG_ARG = 'configuration file or set {env_name}=<path> env variable'

# Environment
ENV_CONFIG_NAME = 'DRDATA_CONFIG'

# Package details
MAIN_DESCRIPTION = 'Dr. Data is a database utility tool that can populate random data based on your schema or can import custom CSV data. See options below'

# Required configuration file
NO_CONFIG_ARGUMENT = 'command requires `-config` argument or set {env_name}=<path/to/file> env variable'
NO_CONFIG_FILE = '`-config={path}` does not exist.'
NO_ARGUMENTS = 'Please choose a command argument (transplant, inject, biopsy, cleanse)'

# Transplant messages
TRANSPLANT_NO_SOURCE = '`--transplant` command requires `-source` argument.'
TRANSPLANT_NO_DESTINATION = '`--transplant` sub command `-source` is a file and requires a `-destination` argument.'
TRANSPLANT_NOT_CSV = '`--transplant` command requires `-source` argument to be CSV file type'
TRANSPLANT_START_MESSAGE = 'Starting transplant command for {database} database!'
TRANSPLANT_COMPLETE_MESSAGE = 'Completed transplant for {database} database!'

# Cleanse messages
CLEANSE_COMPLETE_MESSAGE = 'Completed cleanse for {database} database!'

# Biopsy messages
BIOPSY_NO_EXPORT = '`--biopsy` command requires `-export` argument.'
BIOPSY_EXPORT_NOT_EXIST = 'Path {path} does not exist.'
BIOPSY_START_MESSAGE = 'Starting biopsy command for {database} database!'
BIOPSY_COMPLETE_MESSAGE = 'Completed biopsy for {database} database! Exported file located {export_path}'
BIOPSY_GENERATED_SCHEMA = '- Created {filename}.json schema file.'
BIOPSY_GENERATED_INSERT_ORDER_SCHEMA = '- Generated {filename}.json insertion order schema file.'

# Inject messages
INJECT_NO_ROWS = '`--inject` command requires `-rows` argument.'
INJECT_COMPLETE_MESSAGE = 'Completed with inject for {database} database. Totals of {rows} rows injected'
INJECT_NEED_TO_IMPLEMENT_TYPE = '{types} needs to be implementation in get_random_data_by_type'

