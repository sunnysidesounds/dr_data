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
- Works currently only with PostgreSQL

## Installation 
```bash
# with pypi
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

## Examples
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

# Development Setup
````
git clone https://github.com/sunnysidesounds/dr_data
cd dr_data
python -m venv .
venv/bin/pip install -e .
venv/bin/dr-data -h
```


