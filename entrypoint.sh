#!/bin/sh

MODE="${APP_MODE:=web}"

if [ "$MODE" = "web" ]; then
  echo "Running web mode"
  echo "Preparing static files"
  python manage.py collectstatic --no-input --no-color
  echo "Starting webserver"
  gunicorn -b :80 bringel.wsgi
else
  echo "Running worker mode"
  echo "Starting worker"
  celery -A bringel worker -l INFO
fi
