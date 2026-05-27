#!/bin/sh
set -e

echo "Running migrations..."
python manage.py migrate --noinput

echo "Loading initial data if needed..."
python manage.py loaddata data.json || echo "Skipping loaddata (already loaded or no file)"

echo "Starting gunicorn..."
exec gunicorn config.wsgi:application \
    --bind 0.0.0.0:8080 \
    --workers 2 \
    --timeout 60 \
    --access-logfile -
