#!/bin/bash
echo "#####安装系统所需组件#####"
# shellcheck disable=SC2046
project_path="$(pwd)/../"
pip3 install --upgrade pip
# shellcheck disable=SC2164
cd "$project_path"
yum install mysql-server -y
yum install mysql-devel -y
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
cd "$project_path/bin/"
echo "MYSQL_HOST = '$MYSQL_HOST'" >./database_config.py
# shellcheck disable=SC2129
echo "MYSQL_PORT =  $MYSQL_PORT" >>./database_config.py
echo "MYSQL_USERNAME = '$MYSQL_USERNAME'" >>./database_config.py
echo "MYSQL_PASSWORD = '$MYSQL_PASSWORD'" >>./database_config.py
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
mysql -h $MYSQL_HOST -P $MYSQL_PORT -u $MYSQL_USERNAME -p$MYSQL_PASSWORD -e "INSERT INTO antenna.api_key (id, key, update_time, user_id) VALUES (1, '$key', '2022-01-11 15:16:35', 1);"
echo '######导入初始数据######'
mysql -h $MYSQL_HOST -P $MYSQL_PORT -u $MYSQL_USERNAME -p$MYSQL_PASSWORD antenna <"$project_path/bin/config.sql"
echo '######启动前端######'
cd "$project_path/templates/"
yum install npm -y
npm install -g pm2
npm install -g yarn
yarn config set registry https://registry.npm.taobao.org
yarn
yarn start
echo '######前端成功启动######'
echo '######启动后端######'
nohup python3 ./manage.py 0.0.0.0:80 runserver --noreload &
echo '######后端成功启动######'
