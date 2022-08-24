from modules.config.models import Config
from modules.config.serializers import ConfigSerializer, PlatformUpdateSerializer, ProtocalUpdateSerializer
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from modules.config.constants import CONFIG_TYPES
from modules.config.setting import INVITE_TO_REGISTER

from utils.helper import restart


class ConfigViewSet(mixins.ListModelMixin, GenericViewSet):
    queryset = Config.objects.all().order_by("id")
    serializer_class = ConfigSerializer
    permission_classes = (IsAdminUser,)

    def get_paginated_response(self, data):
        _data = {}
        for i in data:
            if i['value'] == "1" or i['value'] == "0":
                i['value'] = bool(int(i['value']))
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
            return Response(data=request.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"code": 0, "message": f"配置参数错误,原因:{e}"}, status=status.HTTP_200_OK)

    @action(methods=["POST"], detail=False, permission_classes=[IsAdminUser, ])
    def protocal_update(self, request, *args, **kwargs):
        """
        更新协议配置
        """
        serializer = ProtocalUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            for k in request.data.keys():
                Config.objects.filter(name=k, type=CONFIG_TYPES.PROTOCAL).update(value=str(request.data[k]))
            return Response(data=request.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"code": 0, "message": f"配置参数错误,原因:{e}"}, status=status.HTTP_200_OK)

    @action(methods=["GET"], detail=False, permission_classes=[AllowAny, ])
    def open_invite(self, requests, *args, **kwargs):
        """
        查看是否开启邀请码设置
        """
        return Response({"open_invite": int(INVITE_TO_REGISTER)}, status=status.HTTP_200_OK)

    @action(methods=["GET"], detail=False, permission_classes=[IsAdminUser, ])
    def platform_restart(self, requests, *args, **kwargs):
        """
        重启平台
        """
        try:
            restart()
            return Response({}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"code": 0, "message": f"配置参数错误,原因:{e}"}, status=status.HTTP_200_OK)
