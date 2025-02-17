#!/bin/bash
echo "Creating migrations for django app"
python manage.py makemigrations
echo "--------------------------------------------"

echo "Running Migrate command"
python manage.py migrate
echo "--------------------------------------------"

echo "Starting server"
python -m gunicorn --bind 0.0.0.0:8000 --workers 3 core.wsgi 