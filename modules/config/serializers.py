from abc import ABC

from modules.config.constants import CONFIG_TYPES
from modules.config.models import Config, DnsConfig
from rest_framework import serializers


class ConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = Config
        fields = ("name", "value")


class DnsConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = DnsConfig
        fields = "__all__"


class DnsConfigSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=True, help_text="配置id")
    domain = serializers.CharField(required=True, help_text="域名")
    value = serializers.ListField(required=True, help_text="解析内容")

    def validate(self, attrs):
        return attrs


class ProtocalUpdateSerializer(serializers.Serializer):
    """
    协议配置序列化器
    """
    # TODO 大写问题, 如后续需要大写，可以用upper()
    JNDI_PORT = serializers.CharField(required=True, help_text="JNDI端口")
    DNS_DOMAIN = serializers.CharField(required=True, help_text="DNS域名")
    NS1_DOMAIN = serializers.CharField(required=True, help_text="NS1域名")
    NS2_DOMAIN = serializers.CharField(required=True, help_text="NS2域名")

    def validate(self, attrs):
        for k in attrs.keys():
            if not Config.objects.filter(name=k, type=CONFIG_TYPES.PROTOCAL).exists():
                raise serializers.ValidationError({k: "配置参数错误,参数名不存在"})
        return attrs


class PlatformUpdateSerializer(serializers.Serializer):
    """
    平台序列化器
    """
    # TODO 大写问题
    PLATFORM_DOMAIN = serializers.CharField(required=True, help_text="平台域名")
    SERVER_IP = serializers.IPAddressField(required=True, help_text="平台IP")
    LOGIN_PATH = serializers.CharField(required=True, help_text="后台注册地址")
    REGISTER_TYPE = serializers.IntegerField(required=True, help_text="注册类型")
    EMAIL_HOST = serializers.CharField(required=True, help_text="注册邮箱")
    EMAIL_PORT = serializers.CharField(required=True, help_text="邮箱服务器端口")
    EMAIL_HOST_USER = serializers.EmailField(required=True, allow_null=True, allow_blank=True, help_text="账户")
    EMAIL_HOST_PASSWORD = serializers.CharField(required=True, allow_null=True, allow_blank=True, help_text="授权码")
    SAVE_MESSAGE_SEVEN_DAYS = serializers.BooleanField(required=True, help_text="是否保留七天内消息")
    OPEN_EMAIL = serializers.BooleanField(required=True, help_text="开放邮箱通知")

    def validate(self, attrs):
        return attrs
