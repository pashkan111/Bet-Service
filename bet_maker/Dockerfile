FROM python:3.10-slim as python
ENV PYTHONUNBUFFERED=true
WORKDIR /app
EXPOSE 8000

FROM python as poetry
RUN python -c 'from urllib.request import urlopen; print(urlopen("https://install.python-poetry.org").read().decode())' | python3 -
COPY pyproject.toml poetry.lock ./
RUN poetry install -n --no-root --no-dev

FROM python as runtime
ENV PATH="/app/.venv/bin:$PATH"
COPY --from=poetry /app /app
COPY . .

RUN chmod +x ./entrypoint.sh

CMD ["./entrypoint.sh"]