FROM alpine:3.16.2

RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.tuna.tsinghua.edu.cn/g' /etc/apk/repositories \
  && apk update \
  && apk --no-cache add python3 py3-pip python3-dev supervisor \
    mariadb-connector-c-dev libc-dev git libffi-dev libxml2-dev \
    libxslt-dev libressl-dev gcc

RUN apk add --no-cache tzdata \
    && cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
    && echo "Asia/Shanghai" > /etc/timezone \
    && apk del tzdata

ADD . /antenna
WORKDIR /antenna
RUN pip3 config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple \
  && pip3 install -r /antenna/requirements.txt

EXPOSE 53 2345 80 21 443

ENTRYPOINT ["docker/entrypoint.sh"]
