#!/bin/sh

project_path="$(pwd)"

wait-for-it -s "$MYSQL_HOST:$MYSQL_PORT"
python3 -m pip install -r requirements.txt
python3 manage.py makemigrations
echo "make migrations success!"
python3 manage.py migrate
echo "migrate success!"

#python3 manage.py runserver 0.0.0.0:80
unlink /run/supervisord.sock
supervisord -n -c /etc/supervisord.conf

