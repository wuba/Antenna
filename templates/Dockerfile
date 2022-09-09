FROM node:16.17.0


ADD . /antenna
WORKDIR /antenna


RUN cd /bin \
    && npm config set registry https://registry.npm.taobao.org \
    && npm install -g vue-cli \
    && PATH=$PATH:./node_modules/.bin \
    && npm install -g pm2  \
    && yarn config set registry https://registry.npm.taobao.org \
    && yarn config set ignore-engines true


EXPOSE 8000

ENTRYPOINT ["docker/entrypoint.sh"]
