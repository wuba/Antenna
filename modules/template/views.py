import os

from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.models import User
from rest_framework.decorators import action
from rest_framework.response import Response

from modules.template.choose_template import load_template
from modules.template.constants import PRIVATE_TYPES, TEMPLATE_TYPES
from modules.template.models import Template, TemplateConfigItem
from modules.template.serializers import TemplateConfigItemSerializer, TemplateInfoSerializer, \
    UpdateTemplateInfoSerializer, DeleteTmplateSerializer
from rest_framework import filters, mixins, status
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.viewsets import GenericViewSet, ModelViewSet, ViewSet
from utils.helper import generate_code


class TemplateViewSet(ModelViewSet):
    queryset = Template.objects.all().order_by("-id")
    serializer_class = TemplateInfoSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filter_fields = ("name", "type", "is_private")
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user_id = self.request.user.id
        return Template.objects.filter(Q(user=user_id) | Q(is_private=PRIVATE_TYPES.PUBLIC))  # 可查看公开组件

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
            name = data["name"]
            title = data["title"]
            description = data["desc"]
            choice_type = request.data["choice_type"]
            is_private = request.data["is_private"]
            template_item_info = request.data["template_item_info"]
            file_name = request.data["file_name"]
            author = User.objects.get(id=self.request.user.id).username
            template_record = Template.objects.create(name=name, title=title, desc=description,
                                                      choice_type=choice_type,
                                                      is_private=is_private, author=author,
                                                      user_id=self.request.user.id, file_name=file_name)
            for template_item in template_item_info:
                item_name = str(template_item["item_name"])
                config = list(template_item["config"])
                TemplateConfigItem.objects.create(name=item_name, config=config, template_id=template_record.id)

            # 将组件文件移动到正式目录
            current_directory = os.path.dirname(os.path.abspath(__file__))
            index_path = f'{current_directory}/depend/tmp/{file_name}'
            new_path = f'{current_directory}/depend/payload/'
            os.system(f'mv {index_path} {new_path}')
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
        choice_type:1,
        is_private:1,
        "url_type":1
        },
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
            template_id = int(request.query_params.get('template', None))
            if not template_id:
                return Response({"code": 0, "message": f"组件值错误"}, status=status.HTTP_200_OK)
            template_record = Template.objects.filter(id=template_id, user_id=self.request.user.id).first()
            if not template_record:
                return Response({"code": 0, "message": f"没有权限查看该组件"}, status=status.HTTP_200_OK)
            name = template_record.name
            title = template_record.title
            description = template_record.desc
            choice_type = template_record.choice_type
            payload = template_record.payload
            is_private = template_record.is_private
            item_record = TemplateConfigItem.objects.filter(template_id=template_id)
            item_info = [{"item_name": item.name, "config": item.config} for item in item_record]
            return Response(
                {"name": name, "title": title, "desc": description, "is_private": is_private,
                 "choice_type": choice_type,
                 "payload": payload, "template_item_info": item_info}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"code": 0, "message": f"错误原因:{e}"}, status=status.HTTP_200_OK)

    @action(methods=["GET"], detail=False, permission_classes=[IsAuthenticated])
    def view_template_code(self, request, *args, **kwargs):
        """
        获取组件的代码
        """
        try:
            user_id = self.request.user.id
            template_id = request.query_params.get('template_id')
            template_obj = Template.objects.get(template_id=template_id, user_id=user_id)
            if not template_obj.exists():
                return Response({"code": 0, "message": f"不存在该组件"}, status=status.HTTP_200_OK)
            filename = template_obj.file_name
            template_type = template_obj.type
            base_path = str(os.path.abspath(os.path.dirname(__file__)))
            # 读取文件内容
            if template_type == TEMPLATE_TYPES.PAYLOAD:
                file_path = base_path + f"/depend/payload/{filename}"
            else:
                file_path = base_path + f"/depend/listen/{filename}"
            file_object = open(file_path, 'r')
            try:
                code = file_object.read()  # 结果为str类型
            finally:
                file_object.close()
            return Response({"code": code}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"code": 0, "message": f"错误原因:{e}"}, status=status.HTTP_200_OK)

    @action(methods=["POST"], detail=False, permission_classes=[IsAuthenticated])
    def update_template_code(self, request, *args, **kwargs):
        """
        修改组件文件代码
        {
        "template_id":1,
        "code":"aaaaa"}
        """
        try:
            user_id = self.request.user.id
            data = request.data
            template_id = data.get('template_id', 0)
            code = data.get('code', '')
            template_obj = Template.objects.get(template_id=template_id, user_id=user_id)
            if not template_obj.exists():
                return Response({"code": 0, "message": f"不存在该组件"}, status=status.HTTP_200_OK)
            filename = template_obj.file_name
            template_type = template_obj.type
            base_path = str(os.path.abspath(os.path.dirname(__file__)))
            # 读取文件内容
            if template_type == TEMPLATE_TYPES.PAYLOAD:
                file_path = base_path + f"/depend/payload/{filename}"
            else:
                file_path = base_path + f"/depend/listen/{filename}"
            file_object = open(file_path, 'w')
            try:
                code = file_object.write(code)  # 结果为str类型
            finally:
                file_object.flush()
                file_object.close()
            return Response({"code": code}, status=status.HTTP_200_OK)
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
    "filename":"xxxx.py",
    "template_item_info": [{
            "item_name": "xss_config_item",
            "config": ["a", "b"]
        },
        {
            "item_name": "xss_config_item2",
            "config": ["a2", "b2"]
        }
    ]
        }
        """
        try:
            data = request.data
            serializer = UpdateTemplateInfoSerializer(data=data, context={'user': request.user})
            serializer.is_valid(raise_exception=True)
            template_id = data["template_id"]
            name = data["name"]
            title = data["title"]
            description = data["desc"]
            payload = request.data["payload"]
            file_name = request.data["file_name"]
            is_private = request.data["is_private"]
            template_item_info = request.data["template_item_info"]
            author = User.objects.get(id=self.request.user.id).username
            Template.objects.filter(id=template_id).update(name=name, title=title, desc=description,
                                                           payload=payload,
                                                           is_private=is_private, author=author,
                                                           user_id=self.request.user.id,
                                                           file_name=file_name)
            # 删除组件配置
            TemplateConfigItem.objects.filter(template_id=template_id).delete()
            for template_item in template_item_info:
                item_name = template_item["item_name"]
                config = list(template_item["config"])
                TemplateConfigItem.objects.create(name=item_name, config=config, template_id=template_id)
            return Response({"code": 1, "message": f"修改成功"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"code": 0, "message": f"错误原因:{e}"}, status=status.HTTP_200_OK)

    @action(methods=["POST"], detail=False, permission_classes=[IsAuthenticated])
    def upload_template(self, request, *args, **kwargs):
        """
        上传组件文件
        """
        code = self.request.FILES.get("code", None)
        if not code:
            return Response({"code": 0, "message": f"上传空文件!"}, status=status.HTTP_200_OK)
        else:
            filename = f'{generate_code(10)}.py'
        base_path = str(os.path.abspath(os.path.dirname(__file__))) + f"/depend/tmp/{filename}"
        destination = open(base_path, 'wb')  # 保存组件文件
        for chunk in code.chunks():  # 分块写入文件
            destination.write(chunk)
        destination.close()
        return Response({"file_name": filename}, status=status.HTTP_200_OK)

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
            Template.objects.filter(id=template_id, user_id=self.request.user.id).delete()
            return Response({"code": 1, "message": "删除组件成功"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"code": 0, "message": f"错误原因:{e}"}, status=status.HTTP_200_OK)

    @action(methods=["GET"], detail=False, permission_classes=[IsAdminUser])
    def initial_template(self, request, *args, **kwargs):
        """
        初始化组件
        """
        try:
            load_template(user_id=self.request.user.id)
            return Response({"code": 1, "message": "加载组件成功"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"code": 0, "message": f"错误原因:{e}"}, status=status.HTTP_200_OK)


class TemplateConfigItemViewSet(mixins.ListModelMixin, GenericViewSet):
    queryset = TemplateConfigItem.objects.all().order_by("-id")
    serializer_class = TemplateConfigItemSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_fields = ("template",)
    permission_classes = (IsAuthenticated,)
