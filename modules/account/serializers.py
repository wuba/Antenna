import datetime
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from modules.account.models import VerifyCode, InviteCode, User
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


class TestEmailSerializer(serializers.Serializer):
    """
    测试邮箱可用性序列化器
    """
    EMAIL_HOST = serializers.CharField(required=True, help_text="邮箱服务器地址")
    EMAIL_PORT = serializers.CharField(required=True, help_text="邮箱服务器端口")
    EMAIL_HOST_USER = serializers.CharField(required=True, help_text="邮箱服务器用户")
    EMAIL_HOST_PASSWORD = serializers.CharField(required=True, help_text="用户授权码")

    def validate(self, attrs):
        config_record = Config.objects.all()
        OLD_EMAIL_HOST = config_record.get(name="EMAIL_HOST").value
        OLD_EMAIL_PORT = config_record.get(name="EMAIL_PORT").value
        OLD_EMAIL_HOST_USER = config_record.get(name="EMAIL_PORT").value
        OLD_EMAIL_HOST_PASSWORD = config_record.get(name="EMAIL_PORT").value
        if OLD_EMAIL_HOST != attrs["EMAIL_HOST"] or OLD_EMAIL_PORT != attrs["EMAIL_PORT"] or OLD_EMAIL_HOST_USER != \
                attrs["EMAIL_HOST_USER"] or OLD_EMAIL_HOST_PASSWORD != attrs["EMAIL_HOST_PASSWORD"]:
            raise serializers.ValidationError('测试数据未保存，请保存后再进行测试')
        del attrs['verify_code']
        return attrs


class InviteCodeSerializer(serializers.ModelSerializer):
    """
    验证码序列化器
    """

    class Meta:
        model = InviteCode
        fields = "__all__"


class UserRegisterSerializer(serializers.ModelSerializer):
    """
    用户注册序列化器
    """
    verify_code = serializers.CharField(required=True, help_text='验证码',
                                        error_messages={
                                            'required': '该字段是必填字段',
                                            'blank': '请输入验证码'
                                        }, write_only=True)
    username = serializers.EmailField(required=True, allow_blank=False, error_messages={
        'required': '该字段是必填字段',
        'blank': '请输入名字'
    }, validators=[UniqueValidator(queryset=User.objects.
                                   all(), message="用户已存在")])
    password = serializers.CharField(required=True, allow_blank=False, min_length=8, max_length=16,
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

    # 对code字段单独验证(validate_+字段名)
    def validate_verify_code(self, verify_code):
        verify_records = VerifyCode.objects.filter(username=self.initial_data['username']).order_by(
            '-create_time').first()
        if verify_records:
            # 判断验证码是否正确
            if verify_records.verify_code != verify_code:
                raise serializers.ValidationError('验证码错误')
            # 判断验证码是否过期
            five_minutes_ago = datetime.datetime.now() - datetime.timedelta(hours=0, minutes=5, seconds=0)  # 获取5分钟之前的时间
            if verify_records.create_time < five_minutes_ago.replace(tzinfo=None):
                raise serializers.ValidationError('验证码过期')
            # 不用将verify_code返回到数据库中，只是做验证
        else:
            raise serializers.ValidationError('验证码错误')
        return verify_code

    def validate_invite_code(self, invite_code=""):
        INVITE_TO_REGISTER = self.context["INVITE_TO_REGISTER"]
        if INVITE_TO_REGISTER != 1:
            return invite_code
        invite_code_record = InviteCode.objects.filter(code=invite_code).exists()
        if not invite_code_record:
            raise serializers.ValidationError('邀请码错误或失效')
        return invite_code

    def validate(self, attrs):
        OPEN_REGISTER = self.context["OPEN_REGISTER"]
        if OPEN_REGISTER != 1:
            raise serializers.ValidationError('禁止注册')
        return attrs


class ForgetPasswordSerializer(serializers.ModelSerializer):
    """
    忘记密码序列化器
    """
    verify_code = serializers.CharField(required=True, help_text='验证码',
                                        error_messages={
                                            'required': '请输入验证码',
                                        })
    username = serializers.EmailField(required=True, allow_blank=False, validators=[], help_text='用户名',
                                      error_messages={
                                          'required': '该字段是必填字段',
                                          'blank': '请输入验证码'
                                      })
    password = serializers.CharField(required=True, allow_blank=False, min_length=8, max_length=16,
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
        username_record = User.objects.filter(username=username)
        if not username_record:
            raise serializers.ValidationError('用户名不存在')
        return username

    def validate_verify_code(self, verify_code):
        verify_records = VerifyCode.objects.filter(username=self.initial_data['username']).order_by(
            '-create_time').first()
        if verify_records:
            # 判断验证码是否正确
            if verify_records.verify_code != verify_code:
                raise serializers.ValidationError('验证码错误')
            # 判断验证码是否过期
            five_minutes_ago = datetime.datetime.now() - datetime.timedelta(hours=0, minutes=1, seconds=0)  # 获取1分钟之前的时间
            if verify_records.create_time < five_minutes_ago:
                raise serializers.ValidationError('验证码过期')
            # 不用将code返回到数据库中，只是做验证
            return verify_code
        else:
            raise serializers.ValidationError('验证码错误')

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

    def validate(self, attrs):
        if attrs["old_password"] == attrs["password"]:
            raise serializers.ValidationError('新密码与旧密码相同')
        if attrs["password"] != attrs["password_confirm"]:
            raise serializers.ValidationError('确认密码与新密码不同')
        return attrs


class UserLoginSerializer(serializers.ModelSerializer):
    """
    用户登录序列化器
    """
    username = serializers.EmailField(required=True, help_text='用户名')
    password = serializers.CharField(required=True, help_text='用户密码')

    class Meta:
        model = User
        fields = ('username', 'password',)
