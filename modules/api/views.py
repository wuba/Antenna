from modules.api.models import ApiKey
from modules.api.serializers import ApiKeySerializer
from modules.config import setting
from rest_framework import filters, mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from utils.helper import generate_code


class ApiKeyViewSet(mixins.ListModelMixin, GenericViewSet):
    queryset = ApiKey.objects.all().order_by("id")
    serializer_class = ApiKeySerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return ApiKey.objects.filter(user=self.request.user)

    @action(methods=["GET"], detail=False, permission_classes=[IsAuthenticated])
    def refresh(self, request, *args, **kwargs):
        """
        刷新apikey
        """
        new_apikey = generate_code(32)
        ApiKey.objects.filter(user=self.request.user).update(key=new_apikey)
        return Response({"key": new_apikey}, status=status.HTTP_200_OK)

    @action(methods=["GET"], detail=False, permission_classes=[IsAuthenticated])
    def url_list(self, request, *args, **kwargs):
        """
        获取api列表
        """
        key = ApiKey.objects.filter(user_id=self.request.user).first().key
        url_list = [
            {
                "url": f"http://{setting.PLATFORM_DOMAIN}/api/v1/messages/manage/api/?apikey={key}",
                "method": "GET",
                "detail": {
                    "uri": "访问的url路径",
                    "task__name": "任务名",
                    "message_type": "消息类型，1为HTTP，2为DNS，3为LDAP，4为RMI",
                },
            }
        ]
        return Response({"urllist": url_list}, status=status.HTTP_200_OK)
