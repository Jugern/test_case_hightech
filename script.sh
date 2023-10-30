#!/bin/bash
./wait-for-it.sh db:${db_port} -- python manage.py makemigrations NewUsers && python manage.py migrate && python manage.py runserver 0.0.0.0:8000