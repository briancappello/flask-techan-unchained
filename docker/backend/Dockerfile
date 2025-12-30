FROM python:3.12

# install ta-lib
RUN curl -L https://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz -o ta-lib.tar.gz
RUN tar -xvzf ta-lib.tar.gz && \
    cd ta-lib && \
    cp /usr/share/automake-$(automake --version | grep "GNU automake" | cut -d ' ' -f 4 | cut -d '.' -f1,2)/config.guess config.guess && \
    ./configure --prefix=/usr \
    && make \
    && make install

# install uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="$PATH:/root/.local/bin"

WORKDIR /usr/src/app

COPY pyproject.toml ./
COPY uv.lock ./
COPY .python-version ./
RUN uv sync --no-dev

COPY backend backend
COPY bundles bundles
COPY db db
COPY templates templates
COPY celery_app.py .
COPY unchained_config.py .

COPY docker/backend/entrypoint.sh .
EXPOSE 5000
ENTRYPOINT ["bash", "entrypoint.sh"]
