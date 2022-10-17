import os

from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response

from modules.template.choose_template import load_template, view_template_code
from modules.template.constants import PRIVATE_TYPES, TEMPLATE_TYPES
from modules.template.models import Template, TemplateConfigItem
from modules.template.serializers import TemplateConfigItemSerializer, TemplateInfoSerializer, \
    UpdateTemplateInfoSerializer, DeleteTmplateSerializer
from rest_framework import filters, mixins, status
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.viewsets import GenericViewSet, ModelViewSet, ViewSet
from utils.helper import generate_code
from django.forms.models import model_to_dict


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
    def write_template_file_path(cls, template_type, file_name, code):
        """
        将代码内容写入组件文件中
        """
        base_path = str(os.path.abspath(os.path.dirname(__file__)))
        # 删除旧文件
        cls.delete_template_file_path(base_path, file_name)
        if template_type == TEMPLATE_TYPES.PAYLOAD:
            file_path = f"/depend/payload/{file_name}"
        else:
            file_path = f"/depend/listen/{file_name}"
        file_path = base_path + file_path
        destination = open(file_path, 'wb')  # 保存组件文件
        try:
            for chunk in code.chunks():  # 分块写入文件
                destination.write(chunk)
        finally:
            destination.close()

    @staticmethod
    def delete_template_file_path(base_path=str(os.path.abspath(os.path.dirname(__file__))), file_name=None):
        """
        删除文件内容
        """
        # 删除旧文件
        os.system(f"rm -r {base_path}/depend/payload/{file_name} && rm -r {base_path}/depend/listen/{file_name}")

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
            del data["template_item_info"]
            data["user_id"] = self.request.user.id
            data["auther"] = self.request.user.username
            file_name = f'{generate_code(10)}.py'
            data["file_name"] = file_name
            template_record = Template.objects.create(**data)
            for template_item in template_item_info:
                item_name = str(template_item["item_name"])
                config = list(template_item["config"])
                TemplateConfigItem.objects.create(name=item_name, config=config, template_id=template_record.id)
            # 本地创建文件
            template_type = data["type"]
            code = data["code"]
            self.write_template_file_path(template_type, file_name, code)
            return Response({"template_id": template_record.id}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"code": 0, "message": f"错误原因:{e}"}, status=status.HTTP_200_OK)

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
            template_record = Template.objects.filter(id=template_id, user_id=self.request.user.id).first()
            if not template_record:
                return Response({"code": 0, "message": f"没有权限查看该组件"}, status=status.HTTP_200_OK)
            template_info = model_to_dict(template_record)
            item_record = TemplateConfigItem.objects.filter(template_id=template_id)
            item_info = [{"item_name": item.name, "config": item.config} for item in item_record]
            template_info["template_item_info"] = item_info
            # 如果code没有及时更新，重新更新数据库
            if template_info["code"] == "this is a test code":
                _code = view_template_code(filename=template_info["file_name"], template_type=template_info["type"])
                template_info["code"] = _code
            del template_info["file_name"]
            return Response(template_info, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"code": 0, "message": f"错误原因:{e}"}, status=status.HTTP_200_OK)

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
            template_id = data["template_id"]
            template_item_info = request.data["template_item_info"]
            del data["template_item_info"]
            data["user_id"] = self.request.user.id
            data["auther"] = self.request.user.username
            Template.objects.filter(id=template_id).update(**data)
            # 删除组件配置
            TemplateConfigItem.objects.filter(template_id=template_id).delete()
            for template_item in template_item_info:
                item_name = template_item["item_name"]
                config = list(template_item["config"])
                TemplateConfigItem.objects.create(name=item_name, config=config, template_id=template_id)
            # 修改文件
            file_name = Template.objects.get(template_id=template_id).file_name
            template_type = data["type"]
            code = data["code"]
            self.write_template_file_path(template_type, file_name, code)
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
            template_obj.delete()
            # 删除组件
            self.delete_template_file_path(file_name)
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
