from django.contrib import auth
from django.contrib.auth.models import update_last_login
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from modules.account.constants import FIRST_LOGIN, REGISTER_TYPE
from modules.account.models import InviteCode, User, VerifyCode
from modules.account.serializers import (ChangePasswordSerializer, EmailSerializer, ForgetPasswordSerializer,
                                         TestEmailSerializer, UserInfoSerializer, UserLoginSerializer,
                                         UserRegisterSerializer)
from modules.api.models import ApiKey
from modules.config import setting
from modules.task.constants import SHOW_DASHBOARD, TASK_STATUS, TASK_TMP
from modules.task.models import Task, TaskConfig, TaskConfigItem
from modules.template.models import Template, TemplateConfigItem
from utils.helper import generate_code, send_mail


class EmailCodeViewSet(mixins.CreateModelMixin, GenericViewSet):
    """
    发送邮箱验证码
    """
    serializer_class = EmailSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data["username"]
        code = generate_code(6)  # 随机生成code
        send_status = send_mail(username, f"验证码:{code}")
        if not send_status:
            return Response({"code": 0, "message": "发送邮件失败"}, status=status.HTTP_200_OK)
        VerifyCode.objects.create(verify_code=code, username=username)  # 保存验证码
        return Response({"email": username}, status=status.HTTP_200_OK)

    @action(methods=['POST'], detail=False, permission_classes=[IsAdminUser])
    def test(self, request, *args, **kwargs):
        """
        测试邮件
        {
        "EMAIL_HOST":"",
        "EMAIL_PORT":"",
        "EMAIL_HOST_USER":"",
        "EMAIL_HOST_PASSWORD":"",
        }
        """
        serializer = TestEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = self.request.user.username
        send_status = send_mail(username, "测试邮件")
        if not send_status:
            return Response({"code": 0, "message": "发送邮件失败"}, status=status.HTTP_200_OK)
        return Response({"email": username}, status=status.HTTP_200_OK)


class TaskCreator:
    @staticmethod
    def create_initial_task(user_id):
        """
        创建初始任务
        """
        task = Task.objects.create(
            name="初始任务",
            user_id=user_id,
            status=TASK_STATUS.OPEN,
            is_tmp=TASK_TMP.FORMAL,
            show_dashboard=SHOW_DASHBOARD.TRUE
        )
        for key_length, template_name, config_item_name in ((4, "DNS", "dns_log"), (4, "HTTP", "http_log")):
            template = Template.objects.get(name=template_name)
            template_config_item = TemplateConfigItem.objects.get(name=config_item_name)
            task_config = TaskConfig.objects.create(task=task, key=generate_code(key_length))
            TaskConfigItem.objects.create(
                value={},
                template_config_item=template_config_item,
                task=task,
                template=template,
                task_config=task_config
            )


class UserViewSet(mixins.ListModelMixin, mixins.UpdateModelMixin, GenericViewSet, ):
    queryset = User.objects.all().order_by("-id")
    serializer_class = UserInfoSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filter_fields = ("username", "is_staff", "is_active")
    permission_classes = (IsAdminUser,)

    @action(methods=["POST"], detail=False, permission_classes=[AllowAny])
    def register(self, request, *args, **kwargs):
        """
        注册用户
        """
        serializer = UserRegisterSerializer(data=request.data,
                                            context={"REGISTER_TYPE": setting.REGISTER_TYPE})
        serializer.is_valid(raise_exception=True)
        username = request.data["username"]
        password = request.data["password"]
        apikey = generate_code(32)
        invite_code = request.data.get("invite_code", "")
        with transaction.atomic():
            user = User.objects.create_user(username=username, password=password)
            if setting.REGISTER_TYPE == REGISTER_TYPE.INVITE:  # 判断是开放邀请注册
                InviteCode.objects.filter(code=invite_code).delete()
            ApiKey.objects.create(user=user, key=apikey)
            TaskCreator().create_initial_task(user.id)
        response_data = {
            "username": username,
            "apikey": apikey
        }
        return Response(response_data, status=status.HTTP_200_OK)

    @action(methods=["POST"], detail=False, permission_classes=[AllowAny])
    def login(self, request, *args, **kwargs):
        """
        用户登录
        """
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data["username"]
        password = serializer.validated_data["password"]
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            Token.objects.filter(user=user).delete()  # 删除原有的Token
            token = Token.objects.create(user=user)
            private = int(user.is_staff)  # 获取用户角色
            return Response({"username": user.username, "token": token.key, "is_staff": private},
                            status=status.HTTP_200_OK)
        return Response({"code": 0, "message": "用户名或密码错误!"}, status=status.HTTP_200_OK)

    @action(methods=["GET"], detail=False, permission_classes=[IsAuthenticated])
    def logout(self, request, *args, **kwargs):
        """
        用户退出
        """
        user = self.request.user
        auth.logout(request)
        Token.objects.get(user_id=user.id).delete()  # 删除原有的Token
        update_last_login(user=user, sender=None)
        return Response({"code": 1, "message": "用户成功退出"}, status=status.HTTP_200_OK)

    @action(methods=["POST"], detail=False, permission_classes=[AllowAny])
    def forget_password(self, request, *args, **kwargs):
        """
        忘记密码，修改密码
        """
        serializer = ForgetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = request.data["username"]
        password = request.data["password"]
        user = User.objects.get(username=username)
        user.set_password(password)
        user.save()
        return Response({"message": "密码修改成功"}, status=status.HTTP_200_OK)

    @action(methods=["POST"], detail=False, permission_classes=[IsAuthenticated])
    def change_password(self, request, *args, **kwargs):
        """
        登陆后修改密码
        """
        serializer = ChangePasswordSerializer(data=request.data, context={"request": self.request})
        serializer.is_valid(raise_exception=True)
        user = request.user
        old_password = serializer.validated_data["old_password"]
        result = user.check_password(old_password)
        if not result:
            return Response({"code": 0, "message": "旧密码错误"}, status=status.HTTP_200_OK)
        user.set_password(serializer.validated_data["password"])
        user.save()
        return Response({"code": 1, "message": "修改密码成功"}, status=status.HTTP_200_OK)

    @action(methods=["GET"], detail=False, permission_classes=[IsAdminUser])
    def invite_code(self, request, *args, **kwargs):
        """
        邀请码生成
        """
        code = generate_code(10)
        code_record = InviteCode(code=code)
        code_record.save()
        return Response({"invite_code": code}, status=status.HTTP_200_OK)

    @action(methods=["GET"], detail=False, permission_classes=[IsAuthenticated])
    def first_login(self, request, *args, **kwargs):
        """
        判断是否为第一次登录
        """
        result = FIRST_LOGIN.TRUE
        if (self.request.user.last_login is None) or self.request.user.last_login == "2022-01-01 00:00:00":
            result = FIRST_LOGIN.FALSE
        return Response({"first_login": result}, status=status.HTTP_200_OK)

    @action(methods=["GET"], detail=False, permission_classes=[AllowAny])
    def api(self, request, *args, **kwargs):
        """
        通过api获取对应token
        """
        apikey = request.query_params.get('apikey', '')

        try:
            key = get_object_or_404(ApiKey, key=apikey)
            if not key.user_id:
                return Response({"code": 0, "message": "key对应的用户不存在"}, status=status.HTTP_400_BAD_REQUEST)
            token, created = Token.objects.get_or_create(user_id=key.user_id)
            return Response({"token": token.key}, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({"code": 0, "message": "apikey错误"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"code": 0, "message": f"发生未知错误: {str(e)}"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
