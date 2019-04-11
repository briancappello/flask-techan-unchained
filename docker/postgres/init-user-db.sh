#!/bin/bash

set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOL
   CREATE USER techan_unchained WITH PASSWORD 'techan_unchained' CREATEDB;
   CREATE DATABASE techan_unchained;
   GRANT ALL PRIVILEGES ON DATABASE techan_unchained TO techan_unchained;
EOL
