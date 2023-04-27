# syntax=docker/dockerfile:1

FROM python:3.11-alpine

ENV POETRY_VERSION=1.3.2 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install curl and poetry
RUN apk add --no-cache curl \
    && curl -sSL https://install.python-poetry.org | POETRY_VERSION=$POETRY_VERSION python3 -

# Expose the Gunicorn port
EXPOSE 8080

# Set the working directory
WORKDIR /app

# Copy the project files
COPY . .

# Install the dependencies and manage static files
RUN /root/.local/bin/poetry config virtualenvs.create false \
    && /root/.local/bin/poetry install --only main --no-root
#    && python manage.py migrate \
#    && python manage.py collectstatic

# Set the entrypoint for Gunicorn
#ENTRYPOINT ["gunicorn", "--bind", "localhost:8080", "--access-logfile", "-", "evanduke.wsgi"]

ENTRYPOINT ["/app/entrypoint.sh"]

