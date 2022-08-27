#!/bin/bash
pid=$(ps -ef | grep "manage.py runserver" | awk '{print $2}')
# shellcheck disable=SC1046
# shellcheck disable=SC1073
if [[ $pid ]]; then
  echo  "$pid"
  kill -9 $pid || true
  else
    echo "#####Django服务不存在#####"
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

