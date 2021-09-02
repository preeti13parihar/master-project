#!/bin/sh

python manage.py makemigrations

python manage.py migrate

gunicorn --bind :9091 --workers 3 foodconnect.wsgi