#!/bin/bash

declare -A libs
libs[fin-models]="https://github.com/briancappello/fin-models.git"
libs[fun]="https://github.com/briancappello/flask-unchained.git"
libs[sqlalchemy-unchained]="https://github.com/briancappello/sqlalchemy-unchained.git"
libs[flask-sqlalchemy-unchained]="https://github.com/briancappello/flask-sqlalchemy-unchained.git"
libs[py-meta-utils]="https://github.com/briancappello/py-meta-utils.git"

mkdir -p libs

if [[ -d ../flask-unchained && ! -L libs/fun ]]; then
  ln -s ../../flask-unchained libs/fun
  echo "Linked ../flask-unchained to libs/fun"
fi

for lib in "${!libs[@]}"
do
  repo=${libs[$lib]}
  if [[ -d "../$lib" && ! -L "libs/$lib" ]]; then
    ln -s "../../$lib" "libs/$lib"
    echo "Linked ../$lib to libs/$lib"
  else
    git clone "$repo" "libs/$lib"
    echo "Cloned $lib to libs/$lib"
  fi
done
