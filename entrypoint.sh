#!/bin/sh

echo "Preparing static files"
python manage.py collectstatic --no-input --no-color

echo "Starting webserver"
gunicorn -b :80 bringel.wsgi
