#!/bin/sh
set -e

PORT="${PORT:-8000}"

# Try to apply migrations but don't hang forever if DB is unreachable
echo "Running migrations..."
python manage.py migrate || {
  echo "Migrate failed, retrying in 5s..."
  sleep 5
  python manage.py migrate
}

# collect static files
python manage.py collectstatic --noinput

# create superuser from env vars if not exists
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
import os
u = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
p = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'admin')
e = os.environ.get('DJANGO_SUPERUSER_EMAIL', '')
if p and not User.objects.filter(username=u).exists():
    User.objects.create_superuser(u, e, p)
" || true

# seed products if none exist
python manage.py seed_products || true

# start gunicorn
exec gunicorn config.wsgi:application --bind 0.0.0.0:$PORT
