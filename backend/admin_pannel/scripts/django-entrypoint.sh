#!/bin/bash

# Collect static files
echo "Collect static files"
python manage.py collectstatic --noinput

# Apply database migrations
echo "Apply database migrations"
python manage.py migrate

# Apply database migrations
echo "Create superuser"
python manage.py createsuperuser --no-input

# Start server
echo "Starting server"
gunicorn --log-level DEBUG --bind 0.0.0.0:8000 admin_pannel.wsgi:application