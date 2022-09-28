from django.db import models
from modules.message.constants import MESSAGE_TYPES
from modules.task.models import Task
from modules.template.models import Template


class Message(models.Model):
    """
    监控指标统计数据表
    """
    domain = models.CharField(max_length=125, help_text='项目域名')
    remote_addr = models.CharField(max_length=64, help_text='远程请求地址')
    uri = models.CharField(max_length=125, null=True, blank=True, help_text='请求路径')
    header = models.CharField(max_length=1024, null=True, blank=True, help_text='请求头')
    content = models.TextField(null=True, blank=True, help_text='自定义接收内容')
    message_type = models.IntegerField(choices=MESSAGE_TYPES.enum_list, default=MESSAGE_TYPES.HTTP,
                                       help_text='消息类型')
    create_time = models.DateTimeField(auto_now_add=True, null=True, blank=True, help_text="创建时间")
    template = models.ForeignKey(Template, related_name='template_message', default=1, on_delete=models.CASCADE,
                                 db_constraint=False, help_text="所属组件")
    task = models.ForeignKey(Task, related_name='task_message', on_delete=models.CASCADE,
                             db_constraint=False, help_text="所属任务", default="")
    html = models.TextField(null=True, blank=True, help_text='接收内容')

    class Meta:
        db_table = 'message'
