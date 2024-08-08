#!/bin/bash

poetry run flask db upgrade

users_already_populated=$(poetry run flask users list | grep "admin@example.com")
if [ -z "$users_already_populated" ]; then
  poetry run flask db import-fixtures
  #poetry run flask finance init
  #poetry run fin init
fi

poetry run flask run --host 0.0.0.0
