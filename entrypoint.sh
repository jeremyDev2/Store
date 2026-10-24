#!/bin/sh
set -e

echo "Waiting for database..."
until python -c "
import os, sys
try:
    import psycopg
    dsn = os.environ.get('DATABASE_URL') or 'postgresql://store:store@db:5432/store'
    conn = psycopg.connect(dsn)
    conn.close()
    sys.exit(0)
except Exception as e:
    print(e, flush=True)
    sys.exit(1)
"; do
  echo "Database not ready, sleeping..."
  sleep 2
done
echo "Database is ready!"

# apply migrations
python manage.py migrate

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
"

# seed products if none exist
python manage.py seed_products

# start gunicorn
exec gunicorn config.wsgi:application --bind 0.0.0.0:8000
