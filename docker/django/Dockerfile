FROM python:3.11.8-alpine3.18

# Install dependencies
RUN apk update && \
    apk add --no-cache postgresql-dev gcc musl-dev

RUN pip install poetry

# Verify the installation
RUN poetry --version

WORKDIR /app

COPY . .

# RUN poetry install --no-root
# RUN source .venv/bin/activate
RUN pip install -r requirements.txt

COPY ./docker/django/start /start
RUN chmod +x /start
