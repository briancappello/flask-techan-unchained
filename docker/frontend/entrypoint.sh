#!/usr/bin/env bash

cd /home/node/techan.js && \
  cat package.json | jq 'del(.devDependencies)' > package-new.json && \
  cp package-new.json package.json && \
  npm link

cd /home/node || exit

npm link techan
npm run dev
