from django.contrib import auth
from django.contrib.auth.models import update_last_login
from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from modules.api.models import ApiKey
from modules.account.models import User, VerifyCode, InviteCode
from modules.account.serializers import UserInfoSerializer, EmailSerializer, UserRegisterSerializer, \
    ForgetPasswordSerializer, UserLoginSerializer, ChangePasswordSerializer, TestEmailSerializer
from modules.task.models import Task, TaskConfig
from modules.template.models import Template, TemplateConfigItem
from utils.helper import generate_code, send_mail
from rest_framework import mixins, status
from modules.task.constants import SHOW_DASHBOARD, TASK_TMP, TASK_STATUS
from modules.task.models import TaskConfigItem
from modules.account.constants import FIRST_LOGIN
from modules.config import setting
from modules.account.constants import REGISTER_TYPE


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
            return Response({"message": "发送邮件失败"}, status=status.HTTP_200_OK)
        return Response({"email": username}, status=status.HTTP_200_OK)


class TaskCreator:
    DNS_CODE_LENGTH = 4
    HTTP_CODE_LENGTH = 4

    def __init__(self, user_id):
        self.user_id = user_id

    def create_initial_task(self):
        """
        创建初始任务
        """
        initial_task = Task.objects.create(
            name="初始任务",
            user_id=self.user_id,
            status=TASK_STATUS.OPEN,
            is_tmp=TASK_TMP.FORMAL,
            show_dashboard=SHOW_DASHBOARD.TRUE
        )

        dns_code = generate_code(self.DNS_CODE_LENGTH)
        dns_task_config = self._create_task_config(initial_task, dns_code, "DNS", "dns_log")
        http_code = generate_code(self.HTTP_CODE_LENGTH)
        http_task_config = self._create_task_config(initial_task, http_code, "HTTP", "http_log")

        return initial_task

    @staticmethod
    def _create_task_config(task, key, template_name, config_item_name):
        """
        创建任务配置项
        """
        template = Template.objects.get(name=template_name)
        template_config_item = TemplateConfigItem.objects.get(name=config_item_name)
        task_config = TaskConfig.objects.create(task=task, key=key)
        TaskConfigItem.objects.create(
            value={},
            template_config_item=template_config_item,
            task=task,
            template=template,
            task_config=task_config
        )

        return task_config


class UserViewSet(mixins.ListModelMixin, mixins.UpdateModelMixin, GenericViewSet, ):
    queryset = User.objects.all().order_by("-id")
    serializer_class = UserInfoSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filter_fields = ("username", "is_staff", "is_active")
    permission_classes = (IsAdminUser,)

    @action(methods=["POST"], detail=False, permission_classes=[AllowAny])
    @transaction.atomic()
    def register(self, request, *args, **kwargs):
        """
        注册用户
        """
        serializer = UserRegisterSerializer(data=request.data,
                                            context={"REGISTER_TYPE": setting.REGISTER_TYPE})
        serializer.is_valid(raise_exception=True)
        username = request.data["username"]
        password = request.data["password"]
        user = User.objects.create_user(username=username, password=password)  # user = serializer.save()
        invite_code = request.data.get("invite_code", "")
        if setting.REGISTER_TYPE == REGISTER_TYPE.INVITE:  # 判断是开放邀请注册
            InviteCode.objects.filter(code=invite_code).delete()
        apikey = generate_code(32)
        ApiKey.objects.create(user=user, key=apikey)
        task_creator = TaskCreator(user_id=user.id)
        task_creator.create_initial_task()
        response_data = {
            "username": username,
            "apikey": apikey
        }
        return Response(response_data,
                        status=status.HTTP_200_OK)

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
            private = int(User.objects.get(username=username).is_staff)  # 获取用户角色
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
