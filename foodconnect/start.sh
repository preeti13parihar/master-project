#!/bin/sh

python manage.py makemigrations

python manage.py migrate

gunicorn --bind :3000 --workers 1 foodconnect.wsgi