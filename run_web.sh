#!/bin/sh

cd mydjangoapp
su -m myuser -c "python manage.py migrate"
su -m myuser -c "python manage.py runserver 0.0.0.0:8000"