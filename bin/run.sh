#!/bin/bash
pid=$(ps -ef | grep python3 | grep manage | awk '{print $2}')
echo $pid
if [[$pid]]; then
  kill -9 $pid
else
  echo "#####Django服务成功关闭#####"
  echo "#####Django启动服务#####"
  nohup python3 $(dirname `readlink -f $0`)/../manage.py runserver 0.0.0.0:8000 --noreload &
  pid=$(ps -ef | grep python3 | grep manage | awk '{print $2}' | wc -l)
  echo $pid
  if [ ! $pid ]; then
    echo "#####Django服务启动失败#####"
  else
    echo "#####Django服务启动成功#####"
  fi
fi
