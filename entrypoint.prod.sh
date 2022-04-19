#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

python manage.py makemigrations --settings=manjaro.settings.production
python manage.py migrate --settings=manjaro.settings.production
python manage.py collectstatic --settings=manjaro.settings.production --no-input --clear
python manage.py update_index --settings=manjaro.settings.production
exec "$@"