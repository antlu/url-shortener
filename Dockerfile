FROM python:3.9-alpine

ENV PATH=/home/user/.poetry/bin:$PATH \
    POETRY_VIRTUALENVS_CREATE=0 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=0 \
    WORKDIR=/usr/local/src/url_shortener \
    FLASK_APP=$WORKDIR/url_shortener \
    FLASK_ENV=development

RUN apk add --no-cache \
    g++ \
    libffi-dev \
    make \
    musl-dev \
    postgresql-dev \
    zeromq-dev

WORKDIR $WORKDIR

COPY pyproject.toml poetry.lock ./

RUN adduser -D user \
    && chown -R user:user ./

USER user

RUN wget https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py -O - | python > /dev/null \
    && poetry install \
    && rm -rf ~/.cache/pypoetry

COPY --chown=user ./ ./

CMD [ "sh", "./docker-entrypoint.sh"]
