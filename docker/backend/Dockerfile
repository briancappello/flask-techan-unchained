FROM python:3.12

RUN curl -L https://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz -o ta-lib.tar.gz
RUN tar -xvzf ta-lib.tar.gz && \
    cd ta-lib && \
    cp /usr/share/automake-1.16/config.guess config.guess && \
    ./configure --prefix=/usr \
    && make \
    && make install

RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="$PATH:/root/.local/bin"

WORKDIR /usr/src/app

COPY pyproject.toml ./
COPY poetry.lock ./
RUN poetry install --no-root

COPY backend backend
COPY bundles bundles
COPY db db
COPY templates templates
COPY celery_app.py .
COPY unchained_config.py .

COPY docker/backend/entrypoint.sh .
EXPOSE 5000
ENTRYPOINT ["bash", "entrypoint.sh"]
