#!/usr/bin/env bash

if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ] ; then
    (cd /opt/app/wiki; python manage.py createsuperuser --no-input)
fi

# Connect to Django wsgi and attach the gunicorn server to port 8010. It is recommended
# to set workers to (2x $num_cores) + 1
(cd /opt/app/wiki; gunicorn wiki.wsgi --user www-data --bind 0.0.0.0:8010 --workers 3) &
nginx -g "daemon off;"