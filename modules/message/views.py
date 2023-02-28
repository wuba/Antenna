from django.http import HttpResponse
from django.shortcuts import render
import re
from django_filters.rest_framework import DjangoFilterBackend
import datetime
from django.db.models.functions import Cast
from django.db.models import DateField
from modules.api.models import ApiKey
from modules.message.models import Message
from modules.message.serializers import MessageFilter, MessageSerializer
from modules.task.models import Task, TaskConfigItem
from modules.template.choose_template import match_template
from modules.template.constants import PRIVATE_TYPES
from modules.message.constants import MESSAGE_TYPES
from modules.template.models import Template
from rest_framework import filters, mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from django.db.models import Avg, Max, Min, Count, Sum, Q
from utils.helper import get_payload, send_message, get_message_type_name, reconstruct_request, get_param_message, \
    send_email_message
from modules.task.constants import TASK_TMP
from modules.config import setting
from utils.helper import is_base64


class MessageView(GenericViewSet, mixins.ListModelMixin, mixins.DestroyModelMixin):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_class = MessageFilter
    filter_fields = ('message_type', 'template__name', 'task', 'content',)
    search_fields = ('create_time', 'task__name', 'domain')
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_id = self.request.user.id
        return Message.objects.filter(task__user__id=user_id).order_by("-id")

    def list(self, request, *args, **kwargs):
        """
        查询消息
        """
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            for i in serializer.data:
                i["message_type"] = get_message_type_name(i["message_type"])  # 兼容消息类型格式
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        for i in serializer.data:
            i["message_type"] = get_message_type_name(i["message_type"])
        return Response(serializer.data)

    @action(methods=['delete'], detail=False, permission_classes=[IsAuthenticated])
    def multiple_delete(self, request, *args, **kwargs):
        """
        批量删除
        """
        delete_id = request.query_params.get('id', None)
        if not delete_id:
            return Response({"message": "删除失败,输入参数格式错误", "code": 0}, status=status.HTTP_200_OK)
        Message.objects.filter(id__in=delete_id.split(',')).delete()
        return Response({"message": "success", "code": 1}, status=status.HTTP_200_OK)

    @staticmethod
    def message_date_count(message_record):
        """
        计算当前时间起，前七天的数据
        """

        now = datetime.datetime.now()
        days = [(now - datetime.timedelta(days=i)).date() for i in range(6, -1, -1)]
        message_count_list = message_record.filter(create_time__gte=days[0]).annotate(
            date=Cast('create_time', DateField())).values('date').annotate(count=Count('id')).values_list('count',
                                                                                                          flat=True)
        message_count_list = list(message_count_list) + [0] * (7 - len(message_count_list))
        list_day = [day.strftime('%m-%d') for day in days]
        result = {"list_day": list_day, "message_count": message_count_list}
        return result

    @staticmethod
    def message_last_list(message_record):
        """
        取最新的五条消息
        """
        message_record = message_record.order_by("-create_time")[:5].select_related("task")
        message_list = [{
            "id": message.id,
            "domain": message.domain,
            "html": message.html,
            "uri": message.uri,
            "header": message.header,
            "remote_addr": message.remote_addr,
            "task_name": message.task.name,
            "message_type": get_message_type_name(message.message_type),
            "create_time": message.create_time,
            "content": message.content,
        } for message in message_record]
        return message_list

    @staticmethod
    def show_dashboard_url(user_id):
        """
        展示在首页的任务的组件链接
        {"xss": "http://xxx.com/xxxx"}
        """
        url_list = []
        task_config_item_record = TaskConfigItem.objects.filter(
            task__user=user_id,
            task__status=1,
            task__show_dashboard=1
        ).select_related('template', 'task_config')

        if not task_config_item_record:  # 如果为空，直接返回空列表
            return url_list

        url_list = [
            {
                "task_name": tci.task.name,
                tci.template.name: get_payload(tci.task_config.key, tci.template.payload)
            } for tci in task_config_item_record[:30]
        ]
        return url_list

    @action(methods=["GET"], detail=False, permission_classes=[IsAuthenticated, ])
    def dashboard(self, request, *args, **kwargs):
        """
        首页内容view
        """
        user_id = self.request.user.id
        current_date = datetime.datetime.now().date()
        # 基本数据计算
        message_record = Message.objects.filter(task__user_id=user_id)

        message_count = message_record.count()
        today_message_count = message_record.filter(create_time__date=current_date).count()

        task_record = Task.objects.filter(user_id=user_id, is_tmp=TASK_TMP.FORMAL)
        task_count = task_record.count()
        today_task_count = task_record.filter(create_time__date=current_date).count()

        template_record = Template.objects.filter(Q(user_id=user_id) | Q(is_private=PRIVATE_TYPES.PUBLIC))
        template_count = template_record.count()
        today_template_count = template_record.filter(create_time__date=current_date).count()

        # 曲线图数据计算
        message_date_count = self.message_date_count(message_record)

        # message最新五个消息
        last_message_list = self.message_last_list(message_record)
        # 展示链接
        show_dashboard_url = self.show_dashboard_url(user_id)

        result = {
            "message_count": message_count,
            "today_message_count": today_message_count,
            "task_count": task_count,
            "today_task_count": today_task_count,
            "template_count": template_count,
            "today_template_count": today_template_count,
            "message_date_count": message_date_count,
            "last_message_list": last_message_list,
            "dashboard_url": show_dashboard_url

        }

        return Response(data=result, status=status.HTTP_200_OK)

    @action(methods=["GET"], detail=False, permission_classes=[AllowAny, ])
    def api(self, request, *args, **kwargs):
        apikey = self.request.query_params.get('apikey', '')
        key = ApiKey.objects.filter(key=apikey).first()
        if not key:
            return Response({"code": 0, "message": "apikey错误"}, status=status.HTTP_400_BAD_REQUEST)
        queryset = self.filter_queryset(Message.objects.filter(task__user=key.user_id)).order_by("-id")
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


def index(request):
    """
    antenna的请求处理
    """
    path = request.path.strip("/")  # 获取路径  /xxxx
    raw_response = reconstruct_request(request)  # 原始报文
    param_list, message_to_base64 = get_param_message(request)
    message = is_base64(message_to_base64)
    host = request.get_host()  # 项目域名
    domain_key = host.split('.')[0]
    url = host + '/' + path
    remote_addr = request.META.get('REMOTE_ADDR', '')  # 请求ip
    regex = re.compile('^HTTP_')
    headers = dict((regex.sub('', header), value) for (header, value) in request.META.items() if
                   header.startswith('HTTP_'))
    # 利用组件返回response
    if path == setting.LOGIN_PATH:
        return render(request, '../static/index.html')
    elif len(path) == 4:
        task_config_item = TaskConfigItem.objects.filter(task_config__key=path, task__status=1).first()  # 是否是开启状态任务
        if task_config_item:
            if task_config_item.template.type == 0 and not message:  # 如果消息为空并且是利用组件
                template_response = match_template(task_config_item, param_list)
                return template_response
            else:
                Message.objects.create(domain=url, remote_addr=remote_addr, uri=path, header=headers,
                                       message_type=MESSAGE_TYPES.HTTP, content=message,
                                       task_id=task_config_item.task_id, html=raw_response,
                                       template_id=task_config_item.template_id)
                send_message(url=url, remote_addr=remote_addr, uri=path, header=headers,
                             message_type=MESSAGE_TYPES.HTTP, content=message, task_id=task_config_item.task_id,
                             raw=raw_response)

    # http 请求日志
    elif len(domain_key) == 4 and domain_key != setting.PLATFORM_DOMAIN.split('.')[0]:
        task_config_item = TaskConfigItem.objects.filter(task_config__key__iexact=domain_key,
                                                         task__status=1).first()
        if task_config_item:
            username = task_config_item.task.user.username
            send_email_message(username, remote_addr)
            Message.objects.create(domain=host, remote_addr=remote_addr, uri=path, header=headers,
                                   message_type=MESSAGE_TYPES.HTTP, content=message,
                                   task_id=task_config_item.task_id,
                                   template_id=task_config_item.template_id, html=raw_response, )
            send_message(url=host, remote_addr=remote_addr, uri=path, header=headers,
                         message_type=MESSAGE_TYPES.HTTP, content=message, task_id=task_config_item.task_id,
                         raw=raw_response)
    return HttpResponse('', content_type='text/html;charset=utf-8')
