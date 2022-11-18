#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE DATABASE celery_results;
    GRANT ALL PRIVILEGES ON DATABASE celery_results TO "$POSTGRES_USER";
EOSQL