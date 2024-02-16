FROM python:3.11.8-alpine3.18

COPY ./docker/mock-db/mock /mock

RUN chmod +x /mock/mock_db

# Install dependencies
RUN apk update \
    && apk add --no-cache postgresql-dev gcc musl-dev

RUN pip install psycopg2-binary

RUN python3 -c "import psycopg2; print(f\"Psycopg2 successfully installed. version: {psycopg2.__version__}\")"

