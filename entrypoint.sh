#!/bin/sh

set -e

# Run migrations
python manage.py migrate

# Populate database as needed
python manage.py populate_database

# Run collectstatic if necessary
python manage.py collectstatic --noinput

# Start the Gunicorn server
exec gunicorn --bind 0.0.0.0:8080 --access-logfile - "evanduke.wsgi"
