import json

from django.http import HttpResponse, HttpResponseRedirect
from modules.template.depend.base import BaseTemplate
from rest_framework.response import Response


class HttpCustomTemplate(BaseTemplate):
    info = [{
        "template_info": {
            "name": "HTTP_CUSTOM",  # 组件名
            "title": "自定义HTTP利用组件",  # 组件展示标题名
            "author": "bios000",  # 组件作者
            "type": 0,  # 组件类型，1是监听0是利用
            "desc": "",  # 组件介绍
            "desc_url": "",  # 组件使用说明链接
            "choice_type": 0,  # 组件选择类型0是单选，1是多选
            "payload": "http://{domain}/{key}",
            "file_name": "http_custom.py"
        },
        "item_info": [{
            "name": "custom_http_html",
            "config": ["value", "headers"],
        },
            {"name": "custom_http_location",
             "config": ["url"],
             },
            {"name": "jsonp_html",
             "config": ["url"], }
        ]
    }]

    def __init__(self):
        super().__init__()

    def custom_http_html(self, item):
        """
        自定义页面返回内容
        """
        value = item["config"]["value"]
        if item["config"]["headers"]:
            headers = json.loads(item["config"]["headers"])
        else:
            headers = {}
        return HttpResponse(content=value, headers=headers)

    def custom_http_location(self, item):
        """
        自定义页面跳转
        """
        return HttpResponseRedirect(item["config"]["url"])

    def jsonp_html(self, item):
        """
        jsonp 利用
        """
        code = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>JSONP劫持测试</title>
</head>
<body>
<script type="text/javascript">
function callbackFunction(data)
        {{
            alert(data);
        }}
</script>
<script type="text/javascript" src="{item["config"]["url"]}callbackFunction"></script>
</body>
</html>"""
        return HttpResponse(code, content_type="text/html; charset=utf-8")

    def generate(self, key, config):
        response = HttpResponse()
        self.key = key
        try:
            for i in config:
                item_name = i["name"]
                for name in self.__dir__():
                    if name == item_name:
                        response = getattr(self, name)(i)
            return response
        except Exception as e:
            import traceback
            traceback.print_exc()
            return Response({'status': 'false', 'message': '操作失败'})
