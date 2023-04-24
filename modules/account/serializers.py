import datetime

from django.core.cache import cache
from django.utils import timezone
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from modules.account.constants import REGISTER_TYPE
from modules.account.models import InviteCode, User, VerifyCode
from modules.config import setting
from modules.config.models import Config


class UserInfoSerializer(serializers.ModelSerializer):
    username = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'is_active', 'is_staff', 'date_joined',)
        extra_kwargs = {
            'is_active': {'default': True},
            'is_staff': {'default': False}}


class EmailSerializer(serializers.Serializer):
    username = serializers.EmailField(required=True, help_text='验证码',
                                      error_messages={
                                          'required': '该字段是必填字段',
                                          'blank': '请输入邮箱地址'
                                      })

    def validate_username(self, username):
        num_time = datetime.datetime.now() - datetime.timedelta(minutes=5)
        if VerifyCode.objects.filter(username=username, create_time__gt=num_time).count() > 10:
            raise serializers.ValidationError('短时间内超过获取验证码次数')
        return username

# TODO: check
# class EmailSerializer(serializers.Serializer):
"""
Todo:在上述示例中，我们使用 Django 内置的缓存系统来实现缓存功能。在序列化器初始化时，我们设置了一个缓存键
email_verify_codes。然后在 validate_username 方法中，我们从缓存中获取已发送验证码的邮箱列表，并检查输入
的邮箱地址是否存在于缓存中。如果存在，我们检查该邮箱地址的发送次数和最近一次发送时间是否符合限制，并更新缓存中该
邮箱地址的发送次数和最近一次发送时间。如果不存在，我们将该邮箱地址添加到缓存中，并设置发送次数为 1，最近一次发送时间
为当前时间。最后，我们返回输入的邮箱地址。"""


#     username = serializers.EmailField(required=True, help_text='验证码',
#                                       error_messages={
#                                           'required': '该字段是必填字段',
#                                           'blank': '请输入邮箱地址'
#                                       })
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.cache_key = 'email_verify_codes'
#
#     def validate_username(self, username):
#         num_time = datetime.datetime.now() - datetime.timedelta(minutes=5)
#
#         # 从缓存中获取已发送验证码的邮箱列表
#         email_codes = cache.get(self.cache_key, {})
#         email_code = email_codes.get(username, {'count': 0, 'last_sent': None})
#
#         # 检查发送次数是否超过限制
#         if email_code['count'] > 10:
#             raise serializers.ValidationError('短时间内超过获取验证码次数')
#
#         # 检查最近一次发送时间是否超过 5 分钟
#         if email_code['last_sent'] is not None and email_code['last_sent'] > num_time:
#             raise serializers.ValidationError('操作过于频繁，请稍后再试')
#
#         # 更新缓存中该邮箱地址的发送次数和最近一次发送时间
#         email_code['count'] += 1
#         email_code['last_sent'] = datetime.datetime.now()
#         email_codes[username] = email_code
#         cache.set(self.cache_key, email_codes, timeout=300)
#
#         return username


class TestEmailSerializer(serializers.Serializer):
    """
    测试邮箱可用性序列化器
    """
    # TODO 参数改为小写, 其他的序列化类似处理
    EMAIL_HOST = serializers.CharField(required=True, help_text="邮箱服务器地址")
    EMAIL_PORT = serializers.CharField(required=True, help_text="邮箱服务器端口")
    EMAIL_HOST_USER = serializers.CharField(required=True, help_text="邮箱服务器用户")
    EMAIL_HOST_PASSWORD = serializers.CharField(required=True, help_text="用户授权码")

    def validate(self, attrs):
        # OLD_EMAIL_HOST, OLD_EMAIL_PORT, OLD_EMAIL_HOST_USER, OLD_EMAIL_HOST_PASSWORD = (
        #     config_record.get(name=name).value for name in ["EMAIL_HOST", "EMAIL_PORT", "EMAIL_HOST_USER", "EMAIL_HOST_PASSWORD"]
        # )
        config_record = Config.objects.all()
        OLD_EMAIL_HOST = config_record.get(name="EMAIL_HOST").value
        OLD_EMAIL_PORT = config_record.get(name="EMAIL_PORT").value
        OLD_EMAIL_HOST_USER = config_record.get(name="EMAIL_HOST_USER").value
        OLD_EMAIL_HOST_PASSWORD = config_record.get(name="EMAIL_HOST_PASSWORD").value
        if OLD_EMAIL_HOST != attrs["EMAIL_HOST"] or OLD_EMAIL_PORT != attrs["EMAIL_PORT"] or OLD_EMAIL_HOST_USER != \
            attrs["EMAIL_HOST_USER"] or OLD_EMAIL_HOST_PASSWORD != attrs["EMAIL_HOST_PASSWORD"]:
            raise serializers.ValidationError('平台配置未保存，请保存后再进行测试')
        return attrs


class InviteCodeSerializer(serializers.ModelSerializer):
    """
    验证码序列化器
    """

    class Meta:
        model = InviteCode
        fields = "__all__"


class VerifyCodeSerializer(serializers.ModelSerializer):
    verify_code = serializers.CharField(required=True, help_text='验证码',
                                        error_messages={
                                            'required': '该字段是必填字段',
                                            'blank': '请输入验证码'
                                        })

    class Meta:
        abstract = True

    def validate_verify_code(self, verify_code):
        user_email = self.initial_data['username']
        try:
            verify_records = VerifyCode.objects.filter(username=user_email).order_by('-create_time').first()
        except VerifyCode.DoesNotExist:
            raise serializers.ValidationError('验证码错误')
        # 判断验证码是否正确
        if verify_records.verify_code != verify_code:
            raise serializers.ValidationError('验证码错误')
        # 判断验证码是否过期
        five_minutes_ago = timezone.now() - datetime.timedelta(minutes=5)
        if verify_records.create_time < five_minutes_ago:
            raise serializers.ValidationError('验证码过期')
        return verify_code


class UserRegisterSerializer(VerifyCodeSerializer):
    """
    用户注册序列化器
    """
    username = serializers.EmailField(required=True, allow_blank=False, error_messages={
        'required': '该字段是必填字段',
        'blank': '请输入名字'
    }, validators=[UniqueValidator(queryset=User.objects.
                                   all(), message="用户已存在")])

    password = serializers.CharField(required=True, allow_blank=False, min_length=6, max_length=16,
                                     help_text='用户密码',
                                     error_messages={
                                         'min_length': '密码不能少于6位', 'required': '该字段是必填字段',
                                         'blank': '请输入密码'})
    invite_code = serializers.CharField(required=False, help_text='邀请码', max_length=10, min_length=10,
                                        error_messages={
                                            'min_length': '不能少于10位', 'max_length': '不能超过10位'})

    class Meta:
        model = User
        fields = ('username', 'password', 'verify_code', 'invite_code',)

    def validate_invite_code(self, invite_code):
        register_type = self.context["REGISTER_TYPE"]
        print(REGISTER_TYPE.INVITE)
        if register_type == REGISTER_TYPE.INVITE:
            if not InviteCode.objects.filter(code=invite_code).exists():
                raise serializers.ValidationError('邀请码错误或失效')
        return invite_code

    def validate(self, attrs):
        register_type = self.context["REGISTER_TYPE"]
        print(REGISTER_TYPE.REFUSE)
        if register_type == REGISTER_TYPE.REFUSE:
            raise serializers.ValidationError('禁止注册')
        return attrs


class ForgetPasswordSerializer(VerifyCodeSerializer):
    """
    忘记密码序列化器
    """
    username = serializers.EmailField(required=True, allow_blank=False, validators=[], help_text='用户名',
                                      error_messages={
                                          'required': '该字段是必填字段',
                                          'blank': '请输入验证码'
                                      })
    password = serializers.CharField(required=True, allow_blank=False, min_length=6, max_length=16,
                                     help_text='用户密码',
                                     validators=[UniqueValidator(queryset=User.objects.
                                                                 filter(username=username), message='密码与之前相同')],
                                     error_messages={
                                         'min_length': '密码不能少于6位', 'required': '该字段是必填字段',
                                         'blank': '请输入密码'})
    password_confirm = serializers.CharField(required=True, allow_blank=False, min_length=6, help_text='用户密码确认',
                                             error_messages={
                                                 'min_length': '密码不能少于6位', 'required': '该字段是必填字段',
                                                 'blank': '请输入确认密码'})

    class Meta:
        model = User
        fields = ('username', 'verify_code', 'password', 'password_confirm')

    def validate_username(self, username):
        if not User.objects.filter(username=username).exists():
            raise serializers.ValidationError('用户名不存在')
        return username

    def validate(self, attrs):
        if attrs["password"] != attrs["password_confirm"]:
            raise serializers.ValidationError('两次密码不同')
        del attrs['verify_code']
        return attrs


class ChangePasswordSerializer(serializers.ModelSerializer):
    """
    修改密码序列化器
    """
    username = serializers.CharField(required=True, allow_blank=False, help_text='用户名')
    old_password = serializers.CharField(required=True, allow_blank=False, help_text='旧用户密码')
    password = serializers.CharField(required=True, allow_blank=False, min_length=6, help_text='用户密码',
                                     error_messages={
                                         'min_length': '密码不能少于6位'})
    password_confirm = serializers.CharField(required=True, allow_blank=False, min_length=6, help_text='用户密码确认',
                                             error_messages={
                                                 'min_length': '密码不能少于6位'})

    class Meta:
        model = User
        fields = ('username', 'old_password', 'password', 'password_confirm')

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError('旧密码不正确')
        return value

    def validate_password_confirm(self, value):
        password = self.initial_data.get('password')
        if password != value:
            raise serializers.ValidationError('确认密码与新密码不同')
        return value

    def validate_password(self, value):
        old_password = self.initial_data.get('old_password')
        if old_password == value:
            raise serializers.ValidationError('新密码与旧密码相同')
        return value


class UserLoginSerializer(serializers.ModelSerializer):
    """
    用户登录序列化器
    """
    username = serializers.EmailField(required=True, help_text='用户名')
    password = serializers.CharField(required=True, help_text='用户密码')

    class Meta:
        model = User
        fields = ('username', 'password',)
