from rest_framework.exceptions import ValidationError

from modules.message.models import Message
from modules.task.models import Task, TaskConfig, TaskConfigItem
from rest_framework import serializers


class TaskConfigItemSerializer(serializers.ModelSerializer):
    """
    任务配置项序列化器
    """

    class Meta:
        model = TaskConfigItem
        fields = "__all__"


class CreateTaskConfigItemSerializer(serializers.Serializer):
    """
    创建组件实例序列化器
    """
    template = serializers.IntegerField(required=True, help_text="组件id")
    template_config_item_list = serializers.JSONField(required=True, help_text="组件配置列表")
    task = serializers.IntegerField(required=True, help_text="任务id")
    url_template = serializers.IntegerField(required=True, help_text="url模板id")


class TaskConfigSerializer(serializers.ModelSerializer):
    """
    任务配置序列化器
    """

    class Meta:
        model = TaskConfig
        fields = ("task",)


class TaskInfoSerializer(serializers.ModelSerializer):
    """
    任务序列化器
    """
    message_counts = serializers.SerializerMethodField()
    callback_url = serializers.URLField(required=True, allow_blank=True, allow_null=True, help_text="回调地址")
    name = serializers.CharField(required=True, allow_null=True, allow_blank=True, help_text="任务名称")
    callback_url_headers = serializers.CharField(required=True, allow_null=True, allow_blank=True,
                                                 help_text="回调地址header头")
    show_dashboard = serializers.BooleanField(required=True, help_text="主页显示")

    class Meta:
        model = Task
        exclude = ("user", "create_time")

    def get_message_counts(self, Task):
        task_id = Task.id
        message_counts = Message.objects.filter(task_id=task_id).count()
        return message_counts


class CreateTaskSerializer(serializers.Serializer):
    """
    创建任务序列化器
    """
    task_id = serializers.IntegerField(required=True)
    task_name = serializers.CharField(required=True)
    callback_url = serializers.URLField(allow_blank=True, allow_null=True, help_text="回调地址")
    callback_url_headers = serializers.CharField(allow_blank=True, allow_null=True, required=True)
    show_dashboard = serializers.BooleanField(required=True)


class DeleteTmpTaskSerializer(serializers.Serializer):
    """
    删除缓存任务序列化器
    """
    task_id = serializers.IntegerField(required=True, help_text="删除缓存任务")

    def validate_task_id(self, task_id):
        if not Task.objects.filter(id=task_id, user_id=self.context["user"].id).exists():
            raise ValidationError('未知的任务id')
