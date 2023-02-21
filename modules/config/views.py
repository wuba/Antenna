import os
from django.db import transaction

from modules.config.models import Config, DnsConfig
from modules.config.serializers import ConfigSerializer, PlatformUpdateSerializer, DnsConfigSerializer
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from modules.config.constants import CONFIG_TYPES
from modules.config import setting
from modules.config.setting import reload_config


class ConfigViewSet(mixins.ListModelMixin, GenericViewSet):
    queryset = Config.objects.all().order_by("id")
    serializer_class = ConfigSerializer
    permission_classes = (IsAdminUser,)

    def get_paginated_response(self, data):
        _data = {}
        for i in data:
            if i['value'] == "1" or i['value'].lower() == "true":
                i['value'] = True
            elif i['value'] == "0" or i['value'].lower() == "false":
                i['value'] = False
            _data[i["name"]] = i['value']
        return Response(_data, status=status.HTTP_200_OK)

    @action(methods=["POST"], detail=False, permission_classes=[IsAdminUser, ])
    def platform_update(self, request, *args, **kwargs):
        """
        更新平台配置
        """
        serializer = PlatformUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            for k in request.data.keys():
                Config.objects.filter(name=k, type=CONFIG_TYPES.PLATFORM).update(value=str(request.data[k]))
            reload_config()
            return Response(data=request.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"code": 0, "message": f"配置参数错误,原因:{e}"}, status=status.HTTP_200_OK)

    @action(methods=["GET"], detail=False, permission_classes=[AllowAny, ])
    def open_invite(self, requests, *args, **kwargs):
        """
        查看是否开启邀请码设置
        """
        flag = False
        if setting.REGISTER_TYPE == 2:
            flag = True
        return Response({"open_invite": int(flag)}, status=status.HTTP_200_OK)


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
            os.system("supervisorctl restart antenna-dns")
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
            domain = data.get('domain')
            value = data.get('value')
            DnsConfig.objects.update_or_create(defaults={"domain": domain, "value": value}, id=_id)
            # 解决事务问题
            transaction.on_commit(func=DnsConfigViewSet.reload_dns)
            return Response(data=request.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"code": 0, "message": f"参数操作错误,原因:{e}"}, status=status.HTTP_200_OK)

    @action(methods=['delete'], detail=False, permission_classes=[IsAdminUser])
    def dns_delete(self, request, *args, **kwargs):
        """
        删除DNS解析配置,
        """
        try:
            delete_id = request.query_params.get('id', None)
            if not delete_id:
                return Response({"message": "删除失败,输入参数格式错误", "code": 0}, status=status.HTTP_200_OK)
            DnsConfig.objects.filter(id=delete_id).delete()
            transaction.on_commit(func=DnsConfigViewSet.reload_dns)
            return Response({"message": "success", "code": 1}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"code": 0, "message": f"参数操作错误,原因:{e}"}, status=status.HTTP_200_OK)
