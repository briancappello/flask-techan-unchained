FROM python:3.6-slim-stretch

ENV PYTHONUNBUFFERED 1

RUN useradd --user-group --create-home --home-dir /flask --shell /bin/false flask

RUN apt-get update && apt-get install -y linux-headers-4.9 make gcc libxml2-dev libxslt-dev

RUN mkdir /installed-manually
WORKDIR /installed-manually

RUN apt-get install -y git curl
RUN curl -L http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz -o ta-lib.tar.gz
RUN tar -xvzf ta-lib.tar.gz &&\
    cd ta-lib &&\
    ./configure --prefix=/usr &&\
    make &&\
    make install
RUN apt-get remove --purge -y curl

WORKDIR /flask/src

RUN pip install -U pip $(cat requirements.txt | grep ^numpy | cut -d ' ' -f 1)

COPY ./requirements-dev.txt requirements-dev.txt
RUN pip install --no-cache-dir -r requirements-dev.txt

COPY ./requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

USER flask
RUN mkdir -p /flask/.cache /flask/.local/share

COPY ./celery_app.py /flask/src/celery_app.py
COPY ./wsgi.py /flask/src/wsgi.py
COPY ./unchained_config.py /flask/src/unchained_config.py
COPY ./backend /flask/src/backend
COPY ./templates /flask/src/templates
COPY ./bundles /flask/src/bundles
COPY ./db /flask/src/db

CMD flask run --host=0.0.0.0
