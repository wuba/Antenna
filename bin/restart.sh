#!/bin/bash
pid=$(ps -ef | grep python3 | grep manage | awk '{print $2}')
# shellcheck disable=SC1046
# shellcheck disable=SC1073
if [[ $pid ]]; then
  kill $pid
  else
    echo "#####Django服务不存在#####"
  pid=$(ps -ef | grep python3 | grep manage | awk '{print $2}')
  if [[ $pid ]]; then
    kill -9 $pid
    echo "#####Django服务已正常关闭#####"
    echo "#####Django启动服务#####"
    cd ../
    nohup python3 manage.py runserver 0.0.0.0:80 &
    pid=$(ps -ef | grep python3 | grep manage | awk '{print $2}')
    if [[ ! $pid ]]; then
      echo "#####Django服务启动失败#####"
    else
      echo "#####Django服务启动成功#####"
    fi
  fi
fi
