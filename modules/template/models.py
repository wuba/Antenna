from django.contrib.auth.models import User
from django.db import models
from modules.template.constants import TEMPLATE_TYPES, PRIVATE_TYPES, CHOICE_TYPES


class Template(models.Model):
    """
    组件基本信息
    """
    name = models.CharField(max_length=125, help_text='模板文件名', unique=True)
    title = models.CharField(max_length=125, default="默认模板名", help_text='模板对外名称', unique=True)
    desc = models.TextField(null=True, blank=True, help_text='模板简介')
    desc_url = models.URLField(null=True, blank=True, help_text="详细描述的地址")
    author = models.CharField(max_length=125, default="58安全", help_text='模板作者')
    user = models.ForeignKey(User, related_name='user_template', on_delete=models.CASCADE,
                             db_constraint=False, help_text="上传作者", default=1)
    type = models.IntegerField(choices=TEMPLATE_TYPES.enum_list, default=TEMPLATE_TYPES.LISTEN,
                               help_text='模板类型')
    choice_type = models.IntegerField(choices=CHOICE_TYPES.enum_list, default=CHOICE_TYPES.SINGLE,
                                      help_text='是否可以多选')
    file_name = models.CharField(max_length=36, null=True, blank=True, help_text='文件名')
    create_time = models.DateTimeField(auto_now_add=True, null=True, blank=True, help_text="创建时间")
    update_time = models.DateTimeField(auto_now=True, null=True, blank=True, help_text="更新时间")
    is_private = models.IntegerField(choices=PRIVATE_TYPES.enum_list, default=PRIVATE_TYPES.PUBLIC,
                                     help_text='开放类型')
    payload = models.TextField(default="http://{domain}/{key}", help_text='利用代码实例')
    code = models.TextField(default="this is a test code", help_text="文件代码")

    class Meta:
        db_table = 'template'


class TemplateConfigItem(models.Model):
    """
    模板模板配置项
    """
    name = models.CharField(max_length=125, help_text='配置项名称', unique=True)
    config = models.JSONField(max_length=125, help_text='外部传递参数', default=list)
    template = models.ForeignKey(Template, related_name='template_template_config_item', on_delete=models.CASCADE,
                                 db_constraint=False, help_text="所属模板")

    class Meta:
        db_table = 'template_config_item'


class UrlTemplate(models.Model):
    payload = models.TextField(default="http://{domain}/{key}", help_text='利用代码实例')
    template = models.ForeignKey(Template, related_name='template_url_template', on_delete=models.CASCADE,
                                  db_constraint=False, help_text="所属模板")

    class Meta:
        db_table = 'template_url'
