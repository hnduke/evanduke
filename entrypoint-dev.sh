#!/bin/sh

set -e

echo "Running migrations"
python manage.py migrate

echo "Populating database"
python manage.py populate_database

echo "Starting Django runserver"
exec python manage.py runserver 0.0.0.0:8000
