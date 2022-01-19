# Doctor Data (beta)
This is a beta version of this tool. Please submit any issues [here](https://github.com/sunnysidesounds/dr_data/issues)

```bash

usage: dr-data [-h] [-transplant] [-source SOURCE] [-destination DESTINATION] [-inject] [-rows ROWS] [-biopsy] [-export EXPORT] [-cleanse] [-config CONFIG]

Dr. Data is a database utility tool that can populate random data based on your schema or can import custom CSV data. See options below

optional arguments:
-h, --help            show this help message and exit
-transplant           Insert one or all CSV files to table
-source SOURCE        Used in conjuctions with `transplant` The CSV source file or directory. if directory, csv filenames need to match table names
-destination DESTINATION Used in conjuctions with `transplant` and `source`. if `source` is a file. destination TABLE is required
-inject               Inserts one or many randomly regenerated rows
-rows ROWS            How may rows do you want to load per table in the database, default is set in configuration
-biopsy               Explicitly exports a schema and table insertion-order JSON files
-export EXPORT        The directory PATH to export the JSON files
-cleanse              Truncates all the values in the database
-config CONFIG        configuration file or set DRDATA_CONFIG=<path> env variable
```
## Prerequisite
- python 3.9.1
- Works currently only with PostgreSQL 13+

## Installation 
```bash
pip install dr-data
````

## Usage
1. Create a `dr_data.json` file with these values and set `DRDATA_CONFIG=<path>` env variable or using `-config=<path>`  parameter
```bash
{
   "db":{
      "host":"localhost",
      "database":"<db_name>",
      "user":"<db_user>",
      "password":"<db_password>",
      "port":"5432"
   }
}
```
2. Then run one of the procedure commands (-inject, -transplant, -cleanse, -biopsy)

## CLI Examples
Example 1: `-inject` random row data into the database
```bash
dr-data -inject -rows=100
```

Example 2: `-transplant` directory with CSV files (multiple CSV files)
Note: CSV columns need to be named the name as the database column names. 
```bash
dr-data -transplant -source=/path/to/source/directory
```

Example 3: `-transplant` one CSV files (single CSV file)
Note: CSV columns need to be named the name as the database column names.
```bash
dr-data -transplant -source=</path/to/source/file.csv> -destination=<table_name>
```

Example 4: `-biopsy` the database, produces a schema.json and insertion-order-schema.json files
```bash
dr-data -biopsy -export=</path/to/export/directory/>
```

Example 5: `-cleanse` the database of all data.
Warning: This can't be undone.
```bash
dr-data -cleanse
```

## SDK Examples
Example 1: Using `Biopsy` class
```python
from dr_data.biopsy import Biopsy

configuration = {...}
schema= Biopsy(configuration).execute_cmd()
```

Example 2: Using `Inject` class 
```python
from dr_data.biopsy import Biopsy
from dr_data.inject import Inject

configuration = {...}
rows = 25
schema= Biopsy(configuration).execute_cmd()
Inject(schema, configuration).execute_cmd(rows)
```

Example 3: Using `Transplant` class (file import)
```python
from dr_data.transplant import Transplant

configuration = {...}
source_file = "/path/to/foobar.csv"
destination_table = "foobar"
transplant = Transplant(configuration)
transplant.execute_file_cmd(source_file, destination_table)
```

Example 4: Using `Transplant` class (directory import)
```python
from dr_data.transplant import Transplant

configuration = {...}
source_directory= "/path/to/foobar"
transplant = Transplant(configuration)
transplant.execute_directory_cmd(source_directory)
```

Example 5: Using `Randoms` class (optional usage)
```python
from dr_data.randoms import Randoms

random_hash = Randoms.get_hash(10) # get random hash value
random_datetime = Randoms.get_datetime() # get random datetime
random_datetime_with_timezone = Randoms.get_datetime_with_timezone() # get random datetime with timezone
random_number = Randoms.get_datetime_with_timezone() # get random number
random_boolean = Randoms.get_boolean() # get random boolean
...
```

# Development Setup
```bash
git clone https://github.com/sunnysidesounds/dr_data
cd dr_data
python -m venv .
venv/bin/pip install -e .
venv/bin/dr-data -h
```
