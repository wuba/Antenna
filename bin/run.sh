#!/bin/bash
# shellcheck disable=SC2009
pid=$(ps -ef | grep python3 | grep "manage.py runserver 0.0.0.0:8001" | awk '{print $2}')
echo "$pid"
if [ "$pid" ]; then
  kill -9 $pid
pid=$(ps -ef | grep python3 | grep "manage.py runserver 0.0.0.0:8001" | awk '{print $2}')
echo "$pid"
if [ ! $pid ]; then
  echo "#####Django服务成功关闭#####"
  echo "#####Django启动服务#####"
  nohup python3 $(pwd)/manage.py runserver 0.0.0.0:8001 &
pid=$(ps -ef | grep python3 | grep "manage.py runserver 0.0.0.0:8001" | awk '{print $2}')
echo "$pid"
if [ ! $pid ]; then
  echo "#####Django服务启动失败#####"
else
  echo "#####Django服务启动成功#####"
fi
fi
fi
