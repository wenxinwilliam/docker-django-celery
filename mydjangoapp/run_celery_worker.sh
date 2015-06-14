#!/bin/sh

su -m myuser -c "celery worker -A mydjangoapp.celeryconf -Q default -n default@%h"