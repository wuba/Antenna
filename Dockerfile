FROM python:3.10.5-alpine

RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.tuna.tsinghua.edu.cn/g' /etc/apk/repositories \
      && apk update \
      && apk --no-cache add mariadb-connector-c-dev libc-dev \
        git libffi-dev libxml2-dev libxslt-dev libressl-dev gcc

ADD . /antenna
WORKDIR /antenna

RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple \
    && pip install -r /antenna/requirements.txt

EXPOSE 53 2345 80

ENTRYPOINT ["docker/entrypoint.sh"]
