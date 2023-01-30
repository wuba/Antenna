yum install mysql-devel
yum install gcc
yum install supervisor
python3 -m pip install -r ../requirements.txt
python3 ../manage.py makemigrations
echo "make migrations success!"
python3 ../manage.py migrate
echo "migrate success!"
cp ../conf/antenna.ini /etc/supervisord.d/antenna.ini
echo "antenna.ini mv success!"

