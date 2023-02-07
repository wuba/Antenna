yum install mysql-devel
yum install python3-devel
yum install gcc
yum install supervisor
pip3 install -U pip setuptools
python3 -m pip install -r ../requirements.txt
python3 ../manage.py makemigrations
echo "make migrations success!"
python3 ../manage.py migrate
echo "migrate success!"
cp ../conf/antenna.ini /etc/supervisord.d/antenna.ini
echo "antenna.ini mv success!"
