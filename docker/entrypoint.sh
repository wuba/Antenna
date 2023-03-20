#!/bin/sh

project_path="$(pwd)"

wait-for-it -s "$MYSQL_HOST:$MYSQL_PORT"
python3 -m pip install -r requirements.txt
python3 manage.py makemigrations
echo "make migrations success!"
python3 manage.py migrate
echo "migrate success!"
python3 manage.py crontab add
echo "crontab add success!"
#python3 manage.py runserver 0.0.0.0:80
echo "mv success!"
mkdir /etc/supervisor.d
mv conf/antenna.ini /etc/supervisor.d/antenna.ini
unlink /run/supervisor/supervisor.sock
supervisord -n -c /etc/supervisord.conf
