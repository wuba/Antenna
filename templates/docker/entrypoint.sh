#!/bin/bash

pm2 delete all
yarn
yarn _prepare
yarn start
