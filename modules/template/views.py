import os

from django.db import transaction
from django.db.models import Q
from django.forms.models import model_to_dict
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet, ViewSet

from modules.template.choose_template import load_template, view_template_code
from modules.template.constants import PRIVATE_TYPES, TEMPLATE_TYPES
from modules.template.models import Template, TemplateConfigItem, UrlTemplate
from modules.template.serializers import (DeleteTmplateSerializer, TemplateConfigItemSerializer, TemplateInfoSerializer,
                                          UpdateTemplateInfoSerializer, UrlTemplateSerializer, )
from utils.helper import generate_code

BASE_PATH = str(os.path.abspath(os.path.dirname(__file__)))


class TemplateViewSet(ModelViewSet):
    queryset = Template.objects.all().order_by("-id")
    serializer_class = TemplateInfoSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filter_fields = ("name", "type", "is_private")
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user_id = self.request.user.id
        return Template.objects.filter(Q(user=user_id) | Q(is_private=PRIVATE_TYPES.PUBLIC))  # 可查看公开组件

    @classmethod
    def _write_file(cls, template_type, file_name, code):
        """
        将代码内容写入组件文件中
        """
        dir_name = TEMPLATE_TYPES.get_key_from_dict(template_type).lower()
        file_path = os.path.join(BASE_PATH, 'depend', dir_name, file_name)

        # 删除旧文件
        cls._delete_file(file_path)
        # 写新文件
        with open(file_path, 'w') as f:
            f.write(code)

    @staticmethod
    def _delete_file(file_path):
        """
        删除文件内容
        """
        # 删除旧文件
        if os.path.exists(file_path):
            os.remove(file_path)

    def create(self, request, *args, **kwargs):
        """
        新增插件
        {
        "name":"xss",
        "title":"xss利用组件",
        "desc":"xss是一个测试组件",
        "choice_type":1,
        "is_private":1,
        "url_type":1
        "type":"",
        "code":"",
        "template_item_info":[
                {
                "item_name":"xss_config_item",
                "config":["a","b"],
                },
                {
                "item_name":"xss_config_item2",
                "config":["a2","b2"],
                }
            ],
        """

        try:
            data = request.data
            serializer = TemplateInfoSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            template_item_info = request.data["template_item_info"]
            file_name = f'{generate_code(10)}.py'
            data["file_name"] = file_name
            data["user_id"] = self.request.user.id
            data["author"] = self.request.user.username
            del data["template_item_info"]
            del data["config"]
            template_record = Template.objects.create(**data)

            TemplateConfigItem.objects.bulk_create([
                TemplateConfigItem(name=item["item_name"], config=item["config"], template=template_record)
                for item in template_item_info
            ])
            # 本地创建文件
            self._write_file(data["type"], file_name, data["code"])
            return Response({"template_id": template_record.id}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"code": 0, "message": f"错误原因:{repr(e)}"}, status=status.HTTP_200_OK)

    @action(methods=["GET"], detail=False, permission_classes=[IsAuthenticated])
    def template_info(self, request, *args, **kwargs):
        """
        展示组件信息
        {
        "template_Info":
        {
        "name":"xss",
        "title":"xss利用组件",
        "description":"xss是一个测试组件",
        "choice_type":1,
        "is_private":1,
        "url_type":1
        },
        "type":1,
        "code":"",
        "payload":"",
        "template_item_info":[
                {
                "item_name":"xss_config_item",
                "config":["a","b"],
                },
                {
                "item_name":"xss_config_item2",
                "config":["a2","b2"],
                }
            ],
        """
        try:
            template_id = int(request.query_params.get('template', 0))
            template_record = Template.objects.filter(
                Q(id=template_id),
                Q(user_id=self.request.user.id) | Q(template_url_template__isnull=True)
            ).prefetch_related('template_url_template').first()

            if not template_record.user:
                return Response({"code": 0, "message": f"没有权限查看该组件"}, status=status.HTTP_200_OK)
            template_info = model_to_dict(template_record)
            item_record = TemplateConfigItem.objects.filter(template_id=template_id).values('name', 'config')
            item_info = [{"item_name": item["name"], "config": item["config"]} for item in item_record]
            template_info["template_item_info"] = item_info

            # 获取payload模板列表
            template_payload_list = [url_template.payload for url_template in
                                     template_record.template_url_template.all()]
            template_info["payload_list"] = template_payload_list

            # 如果code没有及时更新，重新更新数据库
            if template_info["code"] == "this is a test code":
                _code = view_template_code(filename=template_info["file_name"], template_type=template_info["type"])
                template_record.code = _code
                template_record.save()
                template_info["code"] = _code

            del template_info["file_name"]
            return Response(template_info, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"code": 0, "message": f"错误原因:{repr(e)}"}, status=status.HTTP_200_OK)

    @action(methods=["POST"], detail=False, permission_classes=[IsAuthenticated])
    def update_template(self, request, *args, **kwargs):
        """
        修改组件信息
        {
    "template_id": 1,
    "name": "xss",
    "title": "xss利用组件",
    "description": "xss是一个测试组件",
    "choice_type": 1,
    "is_private": 1,
    "url_type": 1,
    "type":1,
    "code":"",
    "payload":"",
    "payload_list":[
    ],
    "template_item_info": [{
            "item_name": "xss_config_item",
            "config": ["a", "b"]
        },
        {
            "item_name": "xss_config_item2",
            "config": ["a2", "b2"]
        }
    ],}
        """
        try:
            data = request.data
            serializer = UpdateTemplateInfoSerializer(data=data, context={'user': request.user})
            serializer.is_valid(raise_exception=True)
            template_id = int(data["template_id"])
            template_item_info = request.data["template_item_info"]
            payload_list = request.data.get("payload_list", [])
            if "payload_list" in data.keys():
                del data["payload_list"]
            del data["template_item_info"]
            del data["template_id"]
            data["user_id"] = self.request.user.id
            data["author"] = self.request.user.username
            if "payload" not in data.keys():
                data["payload"] = Template.objects.filter(id=template_id).first().payload
            # 查询旧有的TemplateConfigItem
            old_config_items = {item.name: item for item in TemplateConfigItem.objects.filter(template_id=template_id)}
            template = Template.objects.select_for_update().get(id=template_id)
            with transaction.atomic():
                # 修改template 本身
                template.__dict__.update(**data)
                template.save()

                # 更新或新增 UrlTemplate
                url_template = []
                if payload_list:
                    for payload in payload_list:
                        payload = payload.strip()
                        obj, created = UrlTemplate.objects.get_or_create(template_id=template_id,payload=payload)
                    # 删除旧数据
                    UrlTemplate.objects.filter(template_id=template_id).exclude(payload__in=payload_list).delete()

                # 更新或新增 TemplateConfigItem
                for template_item in template_item_info:
                    item_name = template_item["item_name"]
                    config = list(template_item["config"])
                    if item_name in old_config_items:
                        old_config_items[item_name].config = config
                        old_config_items[item_name].save()
                    else:
                        TemplateConfigItem.objects.create(name=item_name, config=config, template_id=template_id)

                # 删除不存在于 template_item_info 中的 TemplateConfigItem
                for name, item in old_config_items.items():
                    if name not in [item["item_name"] for item in template_item_info]:
                        old_config_items[name].delete()

            file_name = Template.objects.get(id=template_id).file_name
            template_type = data["type"]
            code = data["code"]

            self._write_file(template_type, file_name, code)
            return Response({"code": 1, "message": f"修改成功"}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"code": 0, "message": f"错误原因:{e}"}, status=status.HTTP_200_OK)

    @action(methods=["POST"], detail=False, permission_classes=[IsAuthenticated])
    def delete_template(self, request, *args, **kwargs):
        """
        删除组件
        {
        "template_id":1
        }
        """
        serializer = DeleteTmplateSerializer(data=request.data, context={"user": self.request.user})
        serializer.is_valid(raise_exception=True)
        try:
            data = request.data
            template_id = int(data.get("template_id", None))
            if not template_id:
                return Response({"code": 0, "message": "组件id为空"}, status=status.HTTP_200_OK)
            template_obj = Template.objects.get(id=template_id, user_id=self.request.user.id)
            file_name = template_obj.file_name
            template_type = template_obj.type
            template_obj.delete()
            # 删除组件
            dir_name = TEMPLATE_TYPES.get_key_from_dict(template_type).lower()
            file_path = os.path.join(BASE_PATH, 'depend', dir_name, file_name)
            self._delete_file(file_path)
            return Response({"code": 1, "message": "删除组件成功"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"code": 0, "message": f"错误原因:{e}"}, status=status.HTTP_200_OK)

    @action(methods=["POST"], detail=False, permission_classes=[IsAuthenticated])
    def upload_template(self, request, *args, **kwargs):
        """
        上传组件文件
        """
        code = self.request.FILES.get("code", None)
        if not code:
            return Response({"code": 0, "message": f"上传文件为空文件!"}, status=status.HTTP_200_OK)
        return Response({"code": code.read()}, status=status.HTTP_200_OK)

    @action(methods=["GET"], detail=False, permission_classes=[IsAdminUser])
    def initial_template(self, request, *args, **kwargs):
        """
        初始化组件
        """
        try:
            load_template()
            return Response({"code": 1, "message": "加载组件成功"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"code": 0, "message": f"错误原因:{e}"}, status=status.HTTP_200_OK)


class TemplateConfigItemViewSet(mixins.ListModelMixin, GenericViewSet):
    queryset = TemplateConfigItem.objects.all().order_by("-id")
    serializer_class = TemplateConfigItemSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_fields = ("template",)
    permission_classes = (IsAuthenticated,)


class UrlTemplateViewSet(mixins.ListModelMixin, GenericViewSet):
    queryset = UrlTemplate.objects.all().order_by("-id")
    serializer_class = UrlTemplateSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_fields = ("template",)
    permission_classes = (IsAuthenticated,)
