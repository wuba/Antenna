FROM ubuntu:22.04

ENV ANTENNA_HOME=/opt/Antenna
ENV MYSQL_HOST=127.0.0.1
ENV MYSQL_PORT=3306
ENV MYSQL_USERNAME=root
ENV MYSQL_PASSWORD=passwd
ENV PLATFORM_DOMAIN=
ENV PLATFORM_IP=127.0.0.1

WORKDIR $ANTENNA_HOME

RUN apt-get update -y

RUN apt-get install -y python3 python3-dev libmysqld-dev npm git

RUN git clone https://github.com/wuba/Antenna.git ${ANTENNA_HOME}

RUN cd ${ANTENNA_HOME} \
    && apt-get install -y python3-pip \
    && python3 -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --upgrade pip\
    && pip3 install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple \
    && pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple cryptography

RUN apt-get install -y mysql-client

COPY ./entrypoint.sh /opt/entrypoint.sh

EXPOSE 80 8000 2345

CMD [ "/bin/bash", "/opt/entrypoint.sh" ]
