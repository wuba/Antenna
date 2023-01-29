python3 -m pip install -r requirements.txt
python3 manage.py makemigrations
echo "make migrations success!"
python3 manage.py migrate
echo "migrate success!"
mv ../conf/antenna.ini /etc/supervisor.d/antenna.ini
echo "antenna.ini mv success!"
unlink /run/supervisord.sock
supervisord -n -c /etc/supervisord.conf
