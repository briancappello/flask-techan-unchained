#!/usr/bin/env bash

cd /home/node/techan.js && \
  npm link && \
  cd /home/node && \
  npm link techanjs

npm run dev
