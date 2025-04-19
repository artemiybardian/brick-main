#!/bin/bash

# Применение миграций
python server/manage.py makemigrations
python server/manage.py migrate

# Сбор статических файлов
python server/manage.py collectstatic --noinput

# Запуск сервера
python server/manage.py runserver 0.0.0.0:8000

