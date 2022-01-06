import os
import psycopg2
import logging
from progress.bar import Bar
from dr_data.static_strings import *
from dr_data.utilities.file import FileUtility

__author__ = AUTHOR
__copyright__ = COPYRIGHT
__license__ = LICENSE

_logger = logging.getLogger(__name__)


class Sql:

    @staticmethod
    def build_columns_query():
        return """select
        table_schema,
        table_name,
        column_name,
        column_default,
        is_nullable::boolean,
        data_type,
        udt_name,
        col_description((table_schema || '."' || table_name || '"')::regclass, ordinal_position)
    from information_schema.columns
    where table_schema = '{schema_name}' and table_name = '{table_name}'
    order by table_schema, table_name, ordinal_position
    """

    @staticmethod
    def build_tables_query():
        return """select
            table_schema,
            table_name,
            obj_description((table_schema || '."' || table_name || '"')::regclass, 'pg_class')
        from information_schema.tables
        where table_schema = '{name}'
        order by table_schema, table_name
        """

    @staticmethod
    def build_insertion_table_order():
        return """WITH RECURSIVE fkeys AS (
                    SELECT conrelid AS source,
                           confrelid AS target
                    FROM pg_constraint
                    WHERE contype = 'f'
                ),
               tables AS (
                   (
                       SELECT oid AS table_name,
                              1 AS level,
                              ARRAY[oid] AS trail,
                              FALSE AS circular
                       FROM pg_class
                       WHERE relkind = 'r'
                         AND NOT relnamespace::regnamespace::text LIKE ANY
                                    (ARRAY['pg_catalog', 'information_schema', 'pg_temp_%'])
                       EXCEPT
                       SELECT source,
                           1,
                           ARRAY[ source ],
                           FALSE
                       FROM fkeys
                   )
                   UNION ALL
                   SELECT fkeys.source,
                          tables.level + 1,
                          tables.trail || fkeys.source,
                          tables.trail @> ARRAY[fkeys.source]
                   FROM fkeys
                            JOIN tables ON tables.table_name = fkeys.target
                   WHERE cardinality(array_positions(tables.trail, fkeys.source)) < 2
               ),
               ordered_tables AS (
                   SELECT DISTINCT ON (table_name)
                table_name,
                level,
                circular
            FROM tables
            ORDER BY table_name, level DESC
                )
            SELECT table_name::regclass,
                   level
            FROM ordered_tables
            ORDER BY level, table_name
            """

    @staticmethod
    def build_column_constraints():
        return """select
            coalesce(table_schema, referenced_schema) as table_schema,
            coalesce(table_name, referenced_table) as table_name,
            coalesce(column_name, referenced_column) as column_name,
            constraint_schema,
            constraint_name,
            constraint_type,
            check_clause,
            referenced_schema,
            referenced_table,
            referenced_column
        
        from information_schema.table_constraints
                 natural full join information_schema.key_column_usage
                 natural full join information_schema.check_constraints
                 inner join (
            select
                table_schema as referenced_schema,
                table_name as referenced_table,
                column_name as referenced_column,
                constraint_name
            from information_schema.constraint_column_usage
        ) as referenced_columns using (constraint_name)
        
        where constraint_schema = '{schema_name}' and table_name = '{table_name}'  and column_name = '{column_name}'
        order by table_schema, table_name, ordinal_position        
        """

    @staticmethod
    def build_values_from_type():
        return """SELECT pg_type.typname AS enumtype,
               pg_enum.enumlabel AS enumlabel
        FROM pg_type
                 JOIN pg_enum
                      ON pg_enum.enumtypid = pg_type.oid
        WHERE pg_type.typname = '{type}'
 """

    @staticmethod
    def build_populate_insert():
        return """INSERT INTO "{table_name}"({columns} ) VALUES %s ON CONFLICT DO NOTHING"""

    @staticmethod
    def build_random_row():
        return "SELECT {columns} FROM {table} ORDER BY random() LIMIT 1"

    @staticmethod
    def build_random_row_where():
        return "SELECT {columns} FROM {table} {query} ORDER BY random() LIMIT 1"
