FROM ubuntu:22.04

ENV ANTENNA_HOME=/opt/Antenna
ENV MYSQL_HOST=127.0.0.1
ENV MYSQL_PORT=3389
ENV MYSQL_USERNAME=root
ENV MYSQL_PASSWORD=passwd
ENV PLATFORM_DOMAIN=
ENV PLATFORM_IP=127.0.0.1

WORKDIR $ANTENNA_HOME

RUN apt-get update -y

RUN apt-get install -y python3 python3-dev libmysqld-dev npm git \
    && git clone https://github.com/wuba/Antenna.git ${ANTENNA_HOME}

RUN cd $ANTENNA_HOME/bin/ \
    && echo "MYSQL_HOST = '$MYSQL_HOST'" >./database_config.py \
    && echo "MYSQL_PORT =  $MYSQL_PORT" >>./database_config.py \
    && echo "MYSQL_USERNAME = '$MYSQL_USERNAME'" >>./database_config.py \
    && echo "MYSQL_PASSWORD = '$MYSQL_PASSWORD'" >>./database_config.py \
    && echo "PLATFORM_DOMAIN = '$PLATFORM_DOMAIN'" >>./database_config.py \
    && echo "PLATFORM_IP = '$PLATFORM_IP'" >>./database_config.py
    
RUN cd "$ANTENNA_HOME/templates/" \
    && echo "http://$PLATFORM_DOMAIN" >./reqUrl.txt

RUN cd "$ANTENNA_HOME" \
    && python3 ./manage.py makemigrations \
    && echo "make migrations success!" \
    && python3 ./manage.py migrate

RUN key=$(echo $RANDOM | md5sum | head -c 32) \
    && mysql -h $MYSQL_HOST -P $MYSQL_PORT -u $MYSQL_USERNAME -p$MYSQL_PASSWORD -e "INSERT INTO antenna.api_key (id, \`key\`, update_time, user_id) VALUES (1, '$key', '2022-08-09 20:12:29.151182', 1);"

RUN mysql -h $MYSQL_HOST -P $MYSQL_PORT -u $MYSQL_USERNAME -p$MYSQL_PASSWORD -e "INSERT INTO antenna.config (id, name, type, value, create_time, update_time) VALUES (1, 'PLATFORM_DOMAIN', 0, '$PLATFORM_DOMAIN', '2022-01-13 14:20:33', '2022-01-13 14:20:34');" \
    && mysql -h $MYSQL_HOST -P $MYSQL_PORT -u $MYSQL_USERNAME -p$MYSQL_PASSWORD -e "INSERT INTO antenna.config (id, name, type, value, create_time, update_time) VALUES (2, 'DNS_DOMAIN', 1, '$PLATFORM_DOMAIN', '2022-01-13 14:22:40', '2022-01-13 14:22:45');" \
    && mysql -h $MYSQL_HOST -P $MYSQL_PORT -u $MYSQL_USERNAME -p$MYSQL_PASSWORD -e "INSERT INTO antenna.config (id, name, type, value, create_time, update_time) VALUES (4, 'NS1_DOMAIN', 1, 'ns1.$PLATFORM_DOMAIN', '2022-01-13 14:23:10', '2022-01-13 14:23:12');" \
    && mysql -h $MYSQL_HOST -P $MYSQL_PORT -u $MYSQL_USERNAME -p$MYSQL_PASSWORD -e "INSERT INTO antenna.config (id, name, type, value, create_time, update_time) VALUES (5, 'NS2_DOMAIN', 1, 'ns2.$PLATFORM_DOMAIN', '2022-01-13 14:23:42', '2022-01-13 14:23:44');" \
    && mysql -h $MYSQL_HOST -P $MYSQL_PORT -u $MYSQL_USERNAME -p$MYSQL_PASSWORD -e "INSERT INTO antenna.config (id, name, type, value, create_time, update_time) VALUES (6, 'SERVER_IP', 1, '$PLATFORM_IP', '2022-01-13 14:25:06', '2022-01-13 14:25:08');" \
    && mysql -h $MYSQL_HOST -P $MYSQL_PORT -u $MYSQL_USERNAME -p$MYSQL_PASSWORD antenna <"$project_path/bin/config.sql"

RUN cd cd "$ANTENNA_HOME/templates/"\
    && npm install -g pm2 \
    && npm install -g yarn \
    && yarn config set registry https://registry.npm.taobao.org \
    && yarn config set ignore-engines true \
    && yarn \
    && yarn _prepare \
    && yarn start

CMD [ "nohup python3 ./manage.py runserver 0.0.0.0:80 --noreload" ]
