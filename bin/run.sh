##!/bin/bash
#pid=$(ps -ef | grep python3 | grep manage | awk '{print $2}')
## shellcheck disable=SC1046
## shellcheck disable=SC1073
#if [[ ! $pid ]]; then
#  echo "#####Django服务未启动,现在启动#####"
#  cd ../
#  echo "#####Django启动服务#####"
#  python3 manage.py runserver 0.0.0.0:80
#  pid=$(ps -ef | grep python3 | grep manage | awk '{print $2}')
#  if [[ ! $pid ]]; then
#    echo "#####Django服务启动失败#####"
#  else
#    echo "#####Django服务启动成功#####"
#  fi
#fi
cp ../conf/antenna.ini /etc/supervisord.d/antenna.ini
echo "antenna.ini cp success!"
unlink /run/supervisor/supervisord.sock
supervisord -c /etc/supervisord.conf
