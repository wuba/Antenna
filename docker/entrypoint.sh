yarn
yarn _prepare
yarn start
cd /opt/antenna
nohup python3 ./manage.py runserver 0.0.0.0:80 --noreload &