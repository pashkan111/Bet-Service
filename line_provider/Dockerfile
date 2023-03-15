FROM python:3.10-slim as python
ENV PYTHONUNBUFFERED=true
WORKDIR /app
# EXPOSE 8002

FROM python as poetry
ENV PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_HOME=/app/poetry/ \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    POETRY_VERSION=1.3.1
ENV PATH=$POETRY_HOME/bin:$PATH

RUN python -c 'from urllib.request import urlopen; print(urlopen("https://install.python-poetry.org").read().decode())' | python3 -
COPY pyproject.toml poetry.lock ./
RUN poetry install -n --no-root --no-dev

FROM python as runtime
ENV PATH="/app/.venv/bin:$PATH"
COPY --from=poetry /app /app
COPY . .
