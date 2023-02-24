# Check if supervisor is installed
if ! command -v supervisorctl &>/dev/null; then
  echo "supervisor is not installed, please run install.sh it first."
  exit 1
fi
cp ../conf/antenna.ini /etc/supervisord.d/antenna.ini
echo "antenna.ini cp success!"

python3 -m pip install -r ../requirements.txt
echo "pip install  success!"
python3 ../manage.py makemigrations
echo "make migrations success!"
python3 ../manage.py migrate
echo "migrate success!"
python3 ../manage.py crontab add
echo "crontab add success!"
unlink /run/supervisor/supervisor.sock
supervisord -c /etc/supervisord.conf
