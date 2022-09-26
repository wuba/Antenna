FROM python:3.10.5-alpine

RUN apk update \
    && apk --no-cache add mariadb-connector-c-dev libc-dev \
        git libffi-dev libxml2-dev libxslt-dev libressl-dev gcc

ADD . /antenna
WORKDIR /antenna

RUN pip install -r /antenna/requirements.txt

EXPOSE 53 2345 80 21 443

ENTRYPOINT ["docker/entrypoint.sh"]
