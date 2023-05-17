import os
import sys

import django
import re
from twisted.internet import reactor
from twisted.internet.protocol import Factory, Protocol

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__) + "../../../../../")
sys.path.append(PROJECT_ROOT)
os.environ['DJANGO_SETTINGS_MODULE'] = 'antenna.settings'
django.setup()

from modules.template.depend.base import *
from modules.message.constants import MESSAGE_TYPES
from modules.message.models import Message
from modules.task.models import TaskConfigItem
from modules.template import choose_template
from utils.helper import send_message, send_email_message


class HTTP(Protocol):

    def __init__(self):
        super().__init__()
        self.html = None
        self.remote_addr = None
        self.uri = None
        self.content = None
        self.key = None
        self.ip = ""
        self.domain = ""

    def dataReceived(self, data):
        content = str(data, encoding="utf-8")
        self.domain = re.findall(r'Host: (.*?)\r\n', content)[0]
        self.key = self.domain.split('.')[0]
        self.content = content
        self.uri = re.findall(r'/(.*?) HTTP', content)[0]
        echo_message = b"""HTTP/1.0 200 OK
Server: 127.0.0.1
Content-Length: 25
Content-Type: text/plain
Connection: Closed
"""
        self.transport.write(echo_message)
        self.transport.loseConnection()

    def connectionMade(self):
        self.remote_addr = self.transport.getPeer().host

    def is_payload(self, path):
        task_config_item = TaskConfigItem.objects.filter(task_config__key=path,
                                                         task__status=1).first()  # 查看是否是开启状态任务下的链接
        if task_config_item:
            if task_config_item.template.type == 0 and not self.message:  # 如果消息为空并且是利用组件
                template_response = choose_template.match_template(task_config_item)
                return template_response
                pass
            else:
                username = task_config_item.task.user.username
                send_email_message(username, self.remote_addr)
                Message.objects.create(domain=self.domain, remote_addr=self.remote_addr, uri=path, header="",
                                       message_type=MESSAGE_TYPES.HTTP, content=self.html,
                                       task_id=task_config_item.task_id,
                                       template_id=task_config_item.template_id)
                send_message(url=self.domain, remote_addr=self.remote_addr, uri=path, header="",
                             message_type=MESSAGE_TYPES.HTTP, content=self.html, task_id=task_config_item.task_id)

    def connectionLost(self, reason):
        flag, task_config_item = hit(self.key, template_name=["HTTP"], iexact=False)
        if flag:
            message_callback(domain=self.domain, remote_addr=self.remote_addr, task_config_item=task_config_item,
                             uri=self.uri, header='', message_type=MESSAGE_TYPES.HTTP, content=self.content)


class HttpTemplate(BaseTemplate):
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
            "file_name": "httplog.py",
        },
        "item_info": [{
            "name": "http_log",
            "config": [],

        }]}]

    def __init__(self):
        super().__init__()


def main():
    try:
        factory = Factory()
        factory.protocol = HTTP
        print("HTTP 协议监听模块已开启 80 port starting listen ...")
        reactor.listenTCP(80, factory, )
        reactor.run()
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()
