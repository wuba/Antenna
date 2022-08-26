FROM node:alpine

WORKDIR /app

COPY . /app

RUN yarn config set registry https://registry.npm.taobao.org/ && \
    yarn install --ignore-engines

EXPOSE 8080

CMD ["yarn", "serve"]

