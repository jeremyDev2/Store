#!/bin/sh

# apply migrations
.venv/bin/python manage.py migrate

# collect static files
.venv/bin/python manage.py collectstatic --noinput

# create superuser from env vars if not exists
.venv/bin/python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
import os
u = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
p = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'admin')
e = os.environ.get('DJANGO_SUPERUSER_EMAIL', '')
if p and not User.objects.filter(username=u).exists():
    User.objects.create_superuser(u, e, p)
"

# seed products if none exist
.venv/bin/python manage.py seed_products --reset

# start gunicorn
exec .venv/bin/gunicorn config.wsgi:application --bind 0.0.0.0:8000
