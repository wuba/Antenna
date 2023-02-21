from django.db import models
from modules.config.constants import CONFIG_TYPES


class Config(models.Model):
    """
    平台配置
    """
    name = models.CharField(max_length=32, help_text='配置名')
    type = models.IntegerField(choices=CONFIG_TYPES.enum_list, default=CONFIG_TYPES.PLATFORM, help_text='配置类型')
    value = models.CharField(max_length=32, null=True, blank=True, help_text='配置内容')
    create_time = models.DateTimeField(auto_now_add=True, null=True, blank=True, help_text="创建时间")
    update_time = models.DateTimeField(auto_now=True, null=True, blank=True, help_text="更新时间")

    class Meta:
        db_table = 'config'


class DnsConfig(models.Model):
    """
    DNS解析配置
    """
    domain = models.CharField(max_length=32, help_text='域名')
    value = models.JSONField(max_length=128, default=list, help_text="解析类型")

    class Meta:
        db_table = 'dnsconfig'
