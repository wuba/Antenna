from django.db import models
from django.contrib.auth.models import User


class VerifyCode(models.Model):
    """
    email 验证码
    """
    # TODO: 这里username能改为email吗？
    username = models.CharField(max_length=124, help_text='注册用户名')
    verify_code = models.CharField(max_length=6, help_text='验证码')
    create_time = models.DateTimeField(auto_now_add=True, null=True, blank=True, help_text="创建时间")

    class Meta:
        db_table = 'verify_code'


class InviteCode(models.Model):
    """
    邀请码
    """
    code = models.CharField(max_length=10, help_text='验证码')
    create_time = models.DateTimeField(auto_now_add=True, null=True, blank=True, help_text="创建时间")

    class Meta:
        db_table = 'invite_code'
