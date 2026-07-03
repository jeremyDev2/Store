#!/bin/sh

# apply migrations
.venv/bin/python manage.py migrate

# collect static files
.venv/bin/python manage.py collectstatic --noinput

# start gunicorn
exec .venv/bin/gunicorn config.wsgi:application --bind 0.0.0.0:8000
