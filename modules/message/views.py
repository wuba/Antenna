import base64
import datetime

from django.http import HttpResponse
from django.shortcuts import render

from django_filters.rest_framework import DjangoFilterBackend

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
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from django.db.models import Avg, Max, Min, Count, Sum, Q
from utils.helper import get_payload, send_message
from modules.task.constants import TASK_TMP
from modules.config.setting import PLATFORM_DOMAIN
from utils.helper import is_base64


class MessageView(GenericViewSet, mixins.ListModelMixin, mixins.DestroyModelMixin):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_class = MessageFilter
    filter_fields = ('message_type', 'template__name', 'task')
    search_fields = ('create_time', 'task__name')
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_id = self.request.user.id
        return Message.objects.filter(task__user__id=user_id).order_by("-id")

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

        today = datetime.datetime.now()
        oneday = datetime.timedelta(days=6)
        message_count_list = list(
            message_record.filter(create_time__gte=today - oneday, ).extra(
                select={"create_time": "DATE_FORMAT(message.create_time,'%%Y-%%m-%%d')"}).values(
                'create_time').annotate(message_count=Count('create_time')))

        def day_get(today):  # 通过for 循环得到天数
            for i in range(0, 7):
                oneday = datetime.timedelta(days=i)
                day = today - oneday
                date_to = datetime.datetime(day.year, day.month, day.day)
                yield str(date_to)[0:10]

        q_time = day_get(today)
        list_day = [obj for obj in q_time][::-1]
        list_message_day_count = []
        index = 0
        for day in list_day:
            if index <= len(message_count_list) - 1 and len(message_count_list) != 0:
                if day == message_count_list[index]["create_time"]:
                    list_message_day_count.append(message_count_list[index]["message_count"])
                    index += 1
                else:
                    list_message_day_count.append(0)
            else:
                list_message_day_count.append(0)
        list_day = [obj[5::] for obj in list_day]  # 解决浏览器兼容问题，只展示年月
        message_date_count = {"list_day": list_day, "message_count": list_message_day_count}
        return message_date_count

    @staticmethod
    def message_last_list(message_record):
        """
        取最新的五条消息
        """
        message_record = message_record.order_by("-create_time")[:5]
        last_message_list = list(message_record.values())
        message_list = []
        for i in last_message_list:
            i["task_name"] = Task.objects.get(id=i["task_id"]).name
            message_list.append(i)
        return message_list

    @staticmethod
    def show_dashboard_url(user_id):
        """
        展示在首页的任务的组件链接
        {"xss": "http://xxx.com/xxxx"}
        """
        url_list = []
        task_config_item_record = TaskConfigItem.objects.filter(task__user=user_id, task__status=1,
                                                                task__show_dashboard=1)
        if task_config_item_record:
            for task_config_item in task_config_item_record:
                payload = task_config_item.template.payload
                key = task_config_item.task_config.key
                template = task_config_item.template.name
                template_result = {"task_name": task_config_item.task.name, template: get_payload(key, payload)}
                if template_result not in url_list:
                    url_list.append(template_result)
                if len(url_list) > 30:
                    break
        return url_list

    @action(methods=["GET"], detail=False, permission_classes=[IsAuthenticated, ])
    def dashboard(self, request, *args, **kwargs):
        """
        首页内容view

        """
        user_id = self.request.user.id
        # 基本数据计算
        message_record = Message.objects.filter(task__user_id=user_id)
        message_count = message_record.count()
        today_message_count = message_record.filter(create_time__gte=datetime.datetime.now().date()).count()
        task_record = Task.objects.filter(user_id=user_id, is_tmp=TASK_TMP.FORMAL)
        task_count = task_record.count()
        today_task_count = task_record.filter(create_time__gte=datetime.datetime.now().date()).count()
        template_record = Template.objects.filter(Q(user_id=user_id) | Q(is_private=PRIVATE_TYPES.PUBLIC))
        template_count = template_record.count()
        today_template_count = template_record.filter(create_time__gte=datetime.datetime.now().date()).count()
        # 曲线图数据计算
        message_date_count = self.message_date_count(message_record)
        # message最新五个消息
        last_message_list = self.message_last_list(message_record)
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
        queryset = self.filter_queryset(Message.objects.filter(task__user=key.user_id))
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class HttplogView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        """
        http请求记录获取
        """
        path = request.path.strip("/")  # 获取路径  /xxxx
        message = is_base64(request.query_params.get('message', ''))  # 获取的参数message
        host = request.get_host()  # 项目域名
        domain_key = host.split('.')[0]
        url = host + '/' + path
        remote_addr = request.META.get('REMOTE_ADDR', '')  # 请求ip
        header = request.META.get('HTTP_USER_AGENT', '')  # 请求头
        # 利用组件返回response
        if len(path) == 4:
            task_config_item = TaskConfigItem.objects.filter(task_config__key=path,
                                                             task__status=1).first()  # 查看是否是开启状态任务下的链接
            if task_config_item:
                if task_config_item.template.type == 0 and not message:  # 如果消息为空并且是利用组件
                    template_response = match_template(task_config_item)
                    return template_response
                else:
                    Message.objects.create(domain=url, remote_addr=remote_addr, uri=path, header=header,
                                           message_type=MESSAGE_TYPES.HTTP, content=message,
                                           task_id=task_config_item.task_id,
                                           template_id=task_config_item.id)
                    send_message(url=url, remote_addr=remote_addr, uri=path, header=header,
                                 message_type=MESSAGE_TYPES.HTTP, content=message, task_id=task_config_item.task_id)
                    return HttpResponse('', content_type='text/html;charset=utf-8')
        # http 请求日志
        elif len(domain_key) == 4 and domain_key != PLATFORM_DOMAIN.split('.')[0]:
            task_config_item = TaskConfigItem.objects.filter(task_config__key=domain_key, task__status=1).first()
            if task_config_item:
                Message.objects.create(domain=url, remote_addr=remote_addr, uri=path, header=header,
                                       message_type=MESSAGE_TYPES.HTTP, content=message,
                                       task_id=task_config_item.task_id,
                                       template_id=task_config_item.id)
                send_message(url=url, remote_addr=remote_addr, uri=path, header=header,
                             message_type=MESSAGE_TYPES.HTTP, content=message, task_id=task_config_item.task_id)
            return HttpResponse('', content_type='text/html;charset=utf-8')
        else:
            return render(request, 'index.html')
