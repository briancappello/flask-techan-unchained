#!/bin/bash

echo "Running migrations..."
uv run flask db upgrade

users_already_populated=$(uv run flask users list | grep "admin@example.com")
if [ -z "$users_already_populated" ]; then
  echo "Loading data..."
  uv run flask db import-fixtures
  uv run flask finance init
  uv run fin init
fi

editable_libs=(
    fin-models
    fun
    sqlalchemy-unchained
    flask-sqlalchemy-unchained
    py-meta-utils
)

for lib in "${editable_libs[@]}"
do
    if [[ -d "libs/$lib" && ! -z "$(ls -A libs/$lib)" ]]; then
        uv add --editable libs/$lib &> /dev/null
        echo "Installed $lib in editable mode"
    fi
done

echo "Starting web server..."
uv run flask run --host 0.0.0.0
