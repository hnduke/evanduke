#!/bin/sh

set -e

echo "Run migrations"
python manage.py migrate

echo "Populate database"
python manage.py populate_database

echo "Run collectstatic"
python manage.py collectstatic --noinput

echo "Start Gunicorn"
exec gunicorn --bind 0.0.0.0:8080 --access-logfile - "evanduke.wsgi"
