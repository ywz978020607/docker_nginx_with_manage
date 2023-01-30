#!/bin/bash

# python django1/manage.py runserver 0.0.0.0:8000 > docker/log/django.log 2>&1

uwsgi --ini django1/uwsgi.ini
# uwsgi --reload uwsgi.pid
# uwsgi --stop uwsgi.pid

# nginx
# nginx -s reload