DO $$
  BEGIN
    IF NOT EXISTS (
      SELECT *
      FROM pg_catalog.pg_user
      WHERE usename = 'adicu'
    ) THEN
      CREATE ROLE adicu LOGIN PASSWORD 'adicu';
    END IF;

    IF NOT EXISTS (
      SELECT *
      FROM information_schema.schemata
      WHERE schema_name = 'density_schema'
    ) THEN
      CREATE SCHEMA density_schema;
      ALTER SCHEMA density_schema OWNER TO adicu;
    END IF;
  END
$$;

CREATE DATABASE density WITH
      OWNER adicu
      ENCODING 'UTF-8'
      LC_CTYPE 'en_US.utf8'
      LC_COLLATE 'en_US.utf8'
      TEMPLATE template0;