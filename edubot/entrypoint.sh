#!/bin/bash
RUN_PORT="8005"
#list files in current directory
ls -la

/venv/bin/activate python manage.py migrate --no-input
/venv/bin/gunicorn config.wsgi:application --bind "0.0.0.0:${RUN_PORT}" --daemon

nginx -g 'daemon off;'
