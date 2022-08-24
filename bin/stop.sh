#!/bin/bash
# shellcheck disable=SC2009
pid=$(ps -ef | grep python3 | grep "manage.py runserver 0.0.0.0:80" | awk '{print $2}')
echo "$pid"
if [ "$pid" ]; then
  kill -9 $pid
pid=$(ps -ef | grep python3 | grep "manage.py runserver 0.0.0.0:80" | awk '{print $2}')
echo "$pid"
if [ ! $pid ]; then
  echo "#####Django服务成功关闭#####"
else
  echo "#####Django服务关闭失败#####"
fi
fi
