#!/bin/bash
echo "#####安装系统所需组件#####"
# shellcheck disable=SC2046
project_path="$(pwd)/../"
pip3 install --upgrade pip
# shellcheck disable=SC2164
cd "$project_path"
yum install mysql-server -y
yum install mysql-devel -y
yum install python3-devel -y
pip3 install -r requirements.txt -i http://pypi.douban.com/simple --trusted-host pypi.douban.com
echo "pip install success!"
echo "#####配置系统连接mysql数据#####"
# shellcheck disable=SC2162
read -p "mysql ip:" MYSQL_HOST
# shellcheck disable=SC2162
read -p "mysql port:" MYSQL_PORT
# shellcheck disable=SC2162
read -p "mysql username:" MYSQL_USERNAME
# shellcheck disable=SC2162
read -p "mysql password:" MYSQL_PASSWORD
read -p "platform domain:" PLATFORM_DOMAIN
read -p "platform domain:" PLATFORM_IP
cd "$project_path/bin/"
echo "MYSQL_HOST = '$MYSQL_HOST'" >./database_config.py
# shellcheck disable=SC2129
echo "MYSQL_PORT =  $MYSQL_PORT" >>./database_config.py
echo "MYSQL_USERNAME = '$MYSQL_USERNAME'" >>./database_config.py
echo "MYSQL_PASSWORD = '$MYSQL_PASSWORD'" >>./database_config.py
echo "PLATFORM_DOMAIN = '$PLATFORM_DOMAIN'" >>./database_config.py
echo "PLATFORM_IP = '$PLATFORM_IP'" >>./database_config.py
cd "$project_path/templates/"
echo "http://$PLATFORM_DOMAIN" >./reqUrl.txt
# shellcheck disable=SC2164
echo "######创建数据库antenna#####"
mysql -h $MYSQL_HOST -P $MYSQL_PORT -u $MYSQL_USERNAME -p$MYSQL_PASSWORD -e "DROP DATABASE antenna;"
mysql -h $MYSQL_HOST -P $MYSQL_PORT -u $MYSQL_USERNAME -p$MYSQL_PASSWORD -e "CREATE DATABASE antenna;"
echo "######创建数据库成功!#######"
cd "$project_path"
python3 ./manage.py makemigrations
echo "make migrations success!"
python3 ./manage.py migrate
echo "migrate success!"
echo "######生成个人api_key######"
key=$(echo $RANDOM | md5sum | head -c 32)
# shellcheck disable=SC2027
mysql -h $MYSQL_HOST -P $MYSQL_PORT -u $MYSQL_USERNAME -p$MYSQL_PASSWORD -e "INSERT INTO antenna.api_key (id, \`key\`, update_time, user_id) VALUES (1, '$key', '2022-08-09 20:12:29.151182', 1);"

echo '######导入初始数据######'
mysql -h $MYSQL_HOST -P $MYSQL_PORT -u $MYSQL_USERNAME -p$MYSQL_PASSWORD -e "INSERT INTO antenna.config (id, name, type, value, create_time, update_time) VALUES (1, 'PLATFORM_DOMAIN', 0, '$PLATFORM_DOMAIN', '2022-01-13 14:20:33', '2022-01-13 14:20:34');"
mysql -h $MYSQL_HOST -P $MYSQL_PORT -u $MYSQL_USERNAME -p$MYSQL_PASSWORD -e "INSERT INTO antenna.config (id, name, type, value, create_time, update_time) VALUES (2, 'DNS_DOMAIN', 1, '$PLATFORM_DOMAIN', '2022-01-13 14:22:40', '2022-01-13 14:22:45');"
mysql -h $MYSQL_HOST -P $MYSQL_PORT -u $MYSQL_USERNAME -p$MYSQL_PASSWORD -e "INSERT INTO antenna.config (id, name, type, value, create_time, update_time) VALUES (4, 'NS1_DOMAIN', 1, 'ns1.$PLATFORM_DOMAIN', '2022-01-13 14:23:10', '2022-01-13 14:23:12');"
mysql -h $MYSQL_HOST -P $MYSQL_PORT -u $MYSQL_USERNAME -p$MYSQL_PASSWORD -e "INSERT INTO antenna.config (id, name, type, value, create_time, update_time) VALUES (5, 'NS2_DOMAIN', 1, 'ns2.$PLATFORM_DOMAIN', '2022-01-13 14:23:42', '2022-01-13 14:23:44');"
mysql -h $MYSQL_HOST -P $MYSQL_PORT -u $MYSQL_USERNAME -p$MYSQL_PASSWORD -e "INSERT INTO antenna.config (id, name, type, value, create_time, update_time) VALUES (6, 'SERVER_IP', 1, '$PLATFORM_IP', '2022-01-13 14:25:06', '2022-01-13 14:25:08');"
mysql -h $MYSQL_HOST -P $MYSQL_PORT -u $MYSQL_USERNAME -p$MYSQL_PASSWORD antenna <"$project_path/bin/config.sql"
echo '######启动前端######'
cd "$project_path/templates/"
yum install npm -y
npm install -g pm2
npm install -g yarn
yarn config set registry https://registry.npm.taobao.org
yarn config set ignore-engines true
yarn
yarn _prepare
yarn start
echo '######前端成功启动######'
echo '######启动后端######'
cd "$project_path"
nohup python3 ./manage.py runserver 0.0.0.0:80 --noreload &
echo '######后端成功启动######'
