#!/bin/bash

poetry run flask db upgrade

users_already_populated=$(poetry run flask users list | grep "admin@example.com")
if [ -z "$users_already_populated" ]; then
  poetry run flask db import-fixtures
  #poetry run flask finance init
  #poetry run fin init
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
        poetry run pip install -e libs/$lib &> /dev/null
        echo "Installed $lib in editable mode"
    fi
done

poetry run flask run --host 0.0.0.0
