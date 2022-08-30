from datetime import datetime

from django.contrib import auth
from django.contrib.auth.models import update_last_login
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
from modules.config.setting import OPEN_REGISTER, INVITE_TO_REGISTER


class EmailCodeViewSet(mixins.CreateModelMixin, GenericViewSet):
    """
    发送邮箱验证码
    """
    serializer_class = EmailSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = request.data["username"]
        code = generate_code(6)  # 随机生成code
        send_status = send_mail(username, "验证码:" + str(code))
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


class UserViewSet(mixins.ListModelMixin, mixins.UpdateModelMixin, GenericViewSet, ):
    queryset = User.objects.all().order_by("-id")
    serializer_class = UserInfoSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filter_fields = ("username", "is_staff", "is_active")
    permission_classes = (IsAdminUser,)

    @staticmethod
    def create_initial_task(user_id):
        """
        创建初始任务
        """
        initial_task = Task.objects.create(name=f"初始任务", user_id=user_id, status=TASK_STATUS.OPEN,
                                           is_tmp=TASK_TMP.FORMAL,
                                           show_dashboard=SHOW_DASHBOARD.TRUE)  # 创建初始任务
        dns_code = generate_code(4)
        dns_task_config = TaskConfig.objects.create(task_id=initial_task.id, key=dns_code)
        TaskConfigItem.objects.create(value={},
                                      template_config_item_id=TemplateConfigItem.objects.get(name="dns_log").id,
                                      task_id=initial_task.id, template_id=Template.objects.get(name="DNS").id,
                                      task_config_id=dns_task_config.id)
        http_code = generate_code(4)
        http_task_config = TaskConfig.objects.create(task_id=initial_task.id, key=http_code)
        TaskConfigItem.objects.create(value={},
                                      template_config_item_id=TemplateConfigItem.objects.get(name="http_log").id,
                                      task_id=initial_task.id, template_id=Template.objects.get(name="HTTP").id,
                                      task_config_id=http_task_config.id)

    @action(methods=["POST"], detail=False, permission_classes=[AllowAny])
    def register(self, request, *args, **kwargs):
        """
        注册用户
        """
        serializer = UserRegisterSerializer(data=request.data,
                                            context={"INVITE_TO_REGISTER": INVITE_TO_REGISTER,
                                                     "OPEN_REGISTER": OPEN_REGISTER})
        serializer.is_valid(raise_exception=True)
        username = request.data["username"]
        password = request.data["password"]
        user = User.objects.create_user(username=username, password=password)
        invite_code = request.data.get("invite_code", "")
        if INVITE_TO_REGISTER == "1":  # 判断是开放邀请注册
            InviteCode.objects.filter(code=invite_code).delete()
        apikey = generate_code(32)
        ApiKey.objects.create(user=user, key=apikey)
        self.create_initial_task(user_id=user.id)
        return Response({"username": username, "apikey": apikey},
                        status=status.HTTP_200_OK)

    @action(methods=["POST"], detail=False, permission_classes=[AllowAny])
    def login(self, request, *args, **kwargs):
        """
        用户登录
        """
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = request.data["username"]
        password = request.data["password"]
        user = auth.authenticate(username=username, password=password)
        if not user:
            return Response({"code": 0, "message": "用户名或密码错误!"}, status=status.HTTP_200_OK)
        Token.objects.filter(user=user).delete()  # 删除原有的Token
        token = Token.objects.create(user=user)
        private = int(User.objects.get(username=username).is_staff)  # 获取用户角色
        return Response({"username": user.username, "token": token.key, "is_staff": private},
                        status=status.HTTP_200_OK)

    @action(methods=["GET"], detail=False, permission_classes=[IsAuthenticated])
    def logout(self, request, *args, **kwargs):
        """
        用户退出
        """
        user = self.request.user
        auth.logout(request)
        Token.objects.filter(user_id=user.id).delete()  # 删除原有的Token
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
        return Response({"username": username, "password": password},
                        status=status.HTTP_200_OK)

    @action(methods=["POST"], detail=False, permission_classes=[IsAuthenticated])
    def change_password(self, request, *args, **kwargs):
        """
        登陆后修改密码
        """
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.get(username=request.data["username"])
        old_password = request.data["old_password"]
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
        user_id = self.request.user.id
        user_record = User.objects.get(id=user_id)
        if not user_record.last_login or user_record.last_login == "2022-01-01 00:00:00":
            result = FIRST_LOGIN.FALSE
            user_record.last_login = datetime.now()
            user_record.save()
        return Response({"first_login": result}, status=status.HTTP_200_OK)
