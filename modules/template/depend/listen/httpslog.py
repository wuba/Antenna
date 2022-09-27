import os
import sys

import django
import re
from twisted.internet import ssl, reactor
from twisted.internet.protocol import Factory, Protocol

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__) + "../../../")
sys.path.append(PROJECT_ROOT)
os.environ['DJANGO_SETTINGS_MODULE'] = 'antenna.settings'
django.setup()

from modules.template.depend.base import BaseTemplate
from modules.message.constants import MESSAGE_TYPES
from modules.message.models import Message
from modules.task.models import TaskConfigItem
from utils.helper import send_message


class HTTPS(Protocol):

    def __init__(self):
        self.content = None
        self.key = None
        self.domain = None
        self.uri = None
        self.remote_addr = None

    def dataReceived(self, data):
        content = str(data, encoding="utf-8")
        self.domain = re.findall(r'Host: (.*?)\r\n', content)[0]
        self.key = self.domain.split('.')[0]
        self.content = content
        print(content)
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

    def connectionLost(self, reason):
        task_config_item = TaskConfigItem.objects.filter(task_config__key=self.key,
                                                         task__status=1).first()
        if task_config_item and task_config_item.template.name == "HTTPS":
            Message.objects.create(domain=self.domain + '/' + self.uri, message_type=MESSAGE_TYPES.HTTPS,
                                   remote_addr=self.remote_addr,
                                   task_id=task_config_item.task_id,
                                   uri=self.uri,
                                   template_id=task_config_item.template_id,
                                   content="", html=self.content)
            send_message(url=self.domain + '/' + self.uri, remote_addr=self.remote_addr, uri=self.uri, header='',
                         message_type=MESSAGE_TYPES.HTTPS, content=self.content,
                         task_id=task_config_item.task_id)


class HttpsTemplate(BaseTemplate):
    info = [{
        "template_info": {
            "name": "HTTPS",  # 组件名
            "title": "HTTPS协议监听组件",  # 组件展示标题名
            "author": "bios000",  # 组件作者
            "type": 1,  # 组件类型，1是监听0是利用
            "desc": "",  # 组件介绍
            "desc_url": "",  # 组件使用说明链接
            "choice_type": 0,  # 组件选择类型0是单选，1是多选
            "payload": "https://{key}.{domain}",
            "file_name": "httpslog.py",
        },
        "item_info": [{
            "name": "https_log",
            "config": [],

        }]}]

    def __init__(self):
        super().__init__()


def main():
    try:
        factory = Factory()
        factory.protocol = HTTPS
        reactor.listenSSL(443, factory,
                          ssl.DefaultOpenSSLContextFactory(f'{PROJECT_ROOT}/depend/listen/keys/server.key',
                                                           f'{PROJECT_ROOT}/depend/listen/keys/server.crt'))
        reactor.run()
        print("HTTPS 协议监听模块已开启 443 port starting listen ...")
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()
