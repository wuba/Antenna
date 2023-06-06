import os
import subprocess

from django.db import transaction

from modules.config.models import Config, DnsConfig
from modules.config.serializers import ConfigSerializer, PlatformUpdateSerializer, DnsConfigSerializer
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from modules.config import setting
from modules.config.setting import reload_config
from utils.helper import *


class ConfigViewSet(mixins.ListModelMixin, GenericViewSet):
    queryset = Config.objects.all().order_by("id")
    serializer_class = ConfigSerializer
    permission_classes = (IsAdminUser,)

    def get_paginated_response(self, data):
        _data = {}
        mapping = {"1": True, "true": True, "0": False, "false": False, "True": True, "False": False}
        for i in data:
            print(i)
            if i["name"] == "REGISTER_TYPE":
                _data[i["name"]] = int(i['value'])
            else:
                _data[i["name"]] = mapping.get(i['value'], i['value'])
        print(_data)
        return Response(_data, status=status.HTTP_200_OK)

    @action(methods=["POST"], detail=False, permission_classes=[IsAdminUser, ])
    def platform_update(self, request, *args, **kwargs):
        """ 更新平台配置 """
        serializer = PlatformUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        for k, v in request.data.items():
            try:
                Config.objects.filter(name=k).update(value=str(v))
            except Exception as e:
                return Response({"code": 0, "message": f"配置参数错误,原因:{e}"}, status=status.HTTP_200_OK)
        transaction.on_commit(func=reload_config)
        return Response(data=request.data, status=status.HTTP_200_OK)

    @action(methods=["GET"], detail=False, permission_classes=[AllowAny, ])
    def open_invite(self, requests, *args, **kwargs):
        """
        查看是否开启邀请码设置
        """
        from modules.account.constants import REGISTER_TYPE
        flag = int(setting.REGISTER_TYPE == REGISTER_TYPE.INVITE)
        return Response({"open_invite": flag}, status=status.HTTP_200_OK)

    @action(methods=["GET"], detail=False, permission_classes=[IsAdminUser, ])
    def check_version(self, requests, *args, **kwargs):
        """
        获取最新版本号
        """
        flag = False
        try:
            latest_version = get_lastest_verson()
            if not latest_version:
                return Response({"code": 0, "message": f"检查更新错误,原因:{e}"}, status=status.HTTP_200_OK)
            print(latest_version)
            current_file_path = os.path.abspath(__file__)
            print(current_file_path)
            with open(f"{current_file_path}/../../../conf/version.ini", "r") as version_file:
                current_version = version_file.read().strip()
                print(f"Current project version: {current_version}")
            # 比较两个版本
            if latest_version != current_version:
                flag = True
                print("There is a new version available on GitHub.")
            return Response({"renewable": flag}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"code": 0, "message": f"检查更新错误,原因:{e}"}, status=status.HTTP_200_OK)


class DnsConfigViewSet(mixins.ListModelMixin, GenericViewSet):
    queryset = DnsConfig.objects.all().order_by("id")
    serializer_class = DnsConfigSerializer
    permission_classes = (IsAdminUser,)

    @staticmethod
    def reload_dns():
        """
        重启dns组件
        """
        try:
            subprocess.Popen(["supervisorctl", "restart", "antenna-dns"], stdout=subprocess.PIPE)
        except Exception as e:
            print(e)

    @action(methods=["POST"], detail=False, permission_classes=[IsAdminUser, ])
    def dns_update(self, request, *args, **kwargs):
        """
        修改dns配置
        {
        "id":1,
        "domain":"*.test.com",
        "value":["127.0.0.1"],
        }
        """
        serializer = DnsConfigSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            data = request.data
            _id = data.get('id')
            domain = request.data.get('domain')
            value = request.data.get('value')
            DnsConfig.objects.update_or_create(defaults={"domain": domain, "value": value}, id=_id)
            # 解决事务问题
            # TODO 是否可以把reload_dns写到 与reload_config同一个文件里
            transaction.on_commit(func=self.reload_dns)
            return Response(data=request.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"code": 0, "message": f"参数操作错误,原因:{e}"}, status=status.HTTP_200_OK)

    @action(methods=['delete'], detail=False, permission_classes=[IsAdminUser])
    def dns_delete(self, request, *args, **kwargs):
        """ 删除DNS解析配置, """
        delete_id = request.query_params.get('id', None)
        if not delete_id:
            return Response({"message": "删除失败,输入参数格式错误", "code": 0}, status=status.HTTP_200_OK)
        try:
            DnsConfig.objects.get(id=delete_id).delete()
            transaction.on_commit(func=self.reload_dns)
            return Response({"message": "success", "code": 1}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"code": 0, "message": f"参数操作错误,原因:{e}"}, status=status.HTTP_200_OK)
