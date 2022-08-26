#!/bin/sh

project_path="$(pwd)"

~/.local/bin/wait-for-it -s "$MYSQL_HOST:$MYSQL_PORT"
python3 manage.py makemigrations
echo "make migrations success!"
python3 manage.py migrate
echo "migrate success!"

python3 manage.py runserver 0.0.0.0:80 --noreload
