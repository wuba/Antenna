import os
import sys
from abc import ABC

import django

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__) + "../../../")
sys.path.append(PROJECT_ROOT)
print(PROJECT_ROOT)
os.environ['DJANGO_SETTINGS_MODULE'] = 'antenna.settings'
django.setup()

from modules.template.depend.base import BaseTemplate


class HttpTemplate(BaseTemplate, ABC):
    info = [{
        "template_info": {
            "name": "HTTP",  # 组件名
            "title": "HTTP协议监听组件",  # 组件展示标题名
            "author": "bios000",  # 组件作者
            "type": 1,  # 组件类型，1是监听0是利用
            "desc": "",  # 组件介绍
            "desc_url": "",  # 组件使用说明链接
            "choice_type": 0,  # 组件选择类型0是单选，1是多选
            "payload": "http://{key}.{domain}/",
            "file_name": "http.py",
        },
        "item_info": [{
            "name": "http_log",
            "config": [],

        }]}]

    def __init__(self):
        super().__init__()
        self.ip = ""
        self.domain = ""


def main():
    pass


if __name__ == '__main__':
    main()
