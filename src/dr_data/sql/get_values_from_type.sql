SELECT pg_type.typname AS enumtype,
       pg_enum.enumlabel AS enumlabel
FROM pg_type
         JOIN pg_enum
              ON pg_enum.enumtypid = pg_type.oid
WHERE pg_type.typname = '{type}'
