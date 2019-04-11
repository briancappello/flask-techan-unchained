FROM node:11.11-stretch-slim

RUN apt-get update -y && apt install -y git

COPY ./package.json /flask/package.json

WORKDIR /flask

RUN npm install

COPY ./frontend /flask/frontend

RUN npm run build:dll
RUN npm run build
