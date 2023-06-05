from django.contrib.auth.models import User
from django.db import models
from modules.task.constants import TASK_TMP, TASK_STATUS, SHOW_DASHBOARD
from modules.template.models import Template, TemplateConfigItem, UrlTemplate


class Task(models.Model):
    """
    任务表
    """
    name = models.CharField(max_length=125, help_text='任务名称')
    user = models.ForeignKey(User, related_name='user_task', on_delete=models.CASCADE,
                             db_constraint=False, help_text="所属用户")
    status = models.BooleanField(choices=TASK_STATUS.enum_list, default=TASK_STATUS.OPEN, help_text='任务状态')
    create_time = models.DateTimeField(auto_now_add=True, null=True, blank=True,
                                       help_text="创建时间")
    update_time = models.DateTimeField(auto_now=True, null=True, blank=True, help_text="更新时间")
    callback_url = models.TextField(null=True, blank=True, default=None, help_text='回调接口')
    callback_url_headers = models.TextField(null=True, blank=True, default="{}", help_text="接口header")
    is_tmp = models.BooleanField(choices=TASK_TMP.enum_list, default=TASK_TMP.TMP, help_text='任务是否为缓存状态')
    show_dashboard = models.BooleanField(choices=SHOW_DASHBOARD.enum_list, default=SHOW_DASHBOARD.FALSE,
                                         help_text="任务是否展示在dashboard")

    class Meta:
        db_table = 'task'


class TaskConfig(models.Model):
    """
    任务配置表
    """
    task = models.ForeignKey(Task, related_name='task_task_config', on_delete=models.CASCADE, db_constraint=False,
                             help_text="所属任务")
    key = models.CharField(max_length=32, help_text='key')

    url_template = models.ForeignKey(UrlTemplate, related_name='url_template_task_config_item',
                                     on_delete=models.CASCADE, db_column=False,
                                     null=True, help_text="链接模板")

    class Meta:
        db_table = 'task_config'


class TaskConfigItem(models.Model):
    """
    任务配置项表
    """
    task_config = models.ForeignKey(TaskConfig, related_name='task_config_task_config_item', null=True,
                                    on_delete=models.CASCADE,
                                    db_constraint=False, help_text="任务配置")
    template_config_item = models.ForeignKey(TemplateConfigItem, related_name='template_config_item_task_config_item',
                                             on_delete=models.CASCADE,
                                             db_constraint=False, help_text="模板配置项", null=True)
    template = models.ForeignKey(Template, related_name="template_task_config_item", on_delete=models.CASCADE,
                                 db_constraint=False, help_text="模板", null=True)
    value = models.JSONField(max_length=255, default=dict, help_text='配置项的值')
    task = models.ForeignKey(Task, related_name='task_task_config_item', null=True, on_delete=models.CASCADE,
                             db_constraint=False, help_text="任务")

    class Meta:
        db_table = 'task_config_item'
