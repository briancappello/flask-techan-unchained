# Flask Techan Unchained

A demo app integrating [Alpaca MarketStore](https://github.com/alpacahq/marketstore) with Python/React. Built using [Flask Unchained](https://github.com/briancappello/flask-unchained) and [techan.js](http://techanjs.org/).

## Table of Contents

* [Deploying to Google Cloud with Kubernetes and Helm](https://github.com/briancappello/flask-techan-unchained#deploying-to-google-cloud-with-kubernetes-and-helm)
* [Running locally](https://github.com/briancappello/flask-techan-unchained#running-locally)
* [TODO](https://github.com/briancappello/flask-techan-unchained#todo)
* [License](https://github.com/briancappello/flask-techan-unchained#license)

## Deploying to Google Cloud with Kubernetes and Helm

See [gke/README.md](https://github.com/briancappello/flask-techan-unchained/blob/master/gke/README.md)

## Running locally

This assumes you're on a reasonably standard \*nix system. (Tested on Linux)

Dependencies:

- Python 3.6+
- Your virtualenv tool of choice (strongly recommended)
- PostgreSQL
- MarketStore
- Redis (used for sessions persistence and the Celery tasks queue)
- node.js & npm (v6 or later recommended, only required for development)
- MailHog (not required, but it's awesome for testing email related tasks)

```bash
# install
git clone git@github.com:briancappello/flask-techan-unchained.git
cd flask-techan-unchained
mkvirtualenv -p /path/to/python3.6 flask-techan-unchained
pip install -r requirements.txt
pip install -r requirements-dev.txt  # for tests

# configure
edit `backend/config.py` as necessary
edit `frontend/app/config.js` as necessary

# set up database
sudo -u postgres -i psql
postgres=# CREATE USER techan_unchained WITH PASSWORD 'techan_unchained';
postgres=# CREATE DATABASE techan_unchained;
postgres=# GRANT ALL PRIVILEGES ON DATABASE techan_unchained TO techan_unchained;
postgres=# \q  # (quit)

# run db migrations
flask db upgrade

# load db fixtures (optional)
flask db import-fixtures

# initialize finance fixtures
flask finance init

# frontend dev server:
npm install
npm run build:dll
npm run start

# backend dev server:
flask run

# backend celery workers:
flask celery worker
```

## TODO

### Deployment

- convert marketstore PersistentVolumeClaim to StatefulSet (probably also want a ssd StorageClass)
- set up email & celery, ensure auth system works (registration/forgot password)
- convert k8s yaml files to Helm charts
- set up CI/CD
- consolidate and parametrize Helm charts so they work on both GKE and MiniKube
- improve development Dockerfiles to support editing code/configs without rebuilding images

### Missing App Features

- implement support for streaming data (realtime quotes)
- implement market overview page
- implement equity detail page
- implement indexes page
- implement index detail page
- implement watchlists page
- implement watchlist detail page
- add trading support (toggle-able between paper & live)
- add positions monitoring / account dashboards

### Frontend

- update to modern Webpack/Babel/React
- should probably convert chart to use [react-stockcharts](https://github.com/rrag/react-stockcharts)

## License

[Apache 2.0](https://github.com/briancappello/flask-techan-unchained/blob/master/LICENSE)
