import os
import sys

import django
import re
from twisted.internet import ssl, reactor
from twisted.internet.protocol import Factory, Protocol, ClientFactory, ServerFactory

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__) + "../../../")
sys.path.append(PROJECT_ROOT)
os.environ['DJANGO_SETTINGS_MODULE'] = 'antenna.settings'
django.setup()

from modules.template.depend.base import BaseTemplate
from modules.config import setting

class ProxyWebProtocol(Protocol):

    def __init__(self):
        self.request = b''

    def connectionMade(self):
        self.transport.write(self.factory.request)
        self.factory.request = b''

    def dataReceived(self, data):
        self.request = data
        self.factory.proxyprotocol.transport.write(self.request)
        self.request = ''

    # self.transport.loseConnection()

    def connectionLost(self, reason):
        pass


class ProxyWebFactory(ClientFactory):
    protocol = ProxyWebProtocol

    def __init__(self, data, pro):
        self.request = data
        self.proxyprotocol = pro

    def clientConnectionFailed(self, connector, reason):
        pass


class ProxyProtocol(Protocol):
    def __init__(self):
        self.host = ''
        self.port = ''
        self.request = ''

    def connectionMade(self):
        self.host = self.transport.getPeer().host
        self.port = self.transport.getPeer().port

    def dataReceived(self, data):
        self.request = data
        index1 = self.request.index(b' ')
        index2 = self.request.index(b' ', index1 + 1)
        if (index1 == -1) or (index2 == -1):
            raise Exception('http url error')
        # part1 = self.request[index1 + 1:index2]
        # index3 = part1.index(b'/', 8)
        # url = part1[7:index3]
        # print('get the url: ', url)
        proxy_factory = ProxyWebFactory(self.request, self)
        reactor.connectTCP(setting.PLATFORM_DOMAIN, 80, proxy_factory)

    # self.transport.loseConnection()

    def connectionLost(self, reason):
        pass


class ProxyFactory(ServerFactory):
    protocol = ProxyProtocol


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
        factory = ProxyFactory()
        reactor.listenSSL(443, factory,
                          ssl.DefaultOpenSSLContextFactory(f'{PROJECT_ROOT}/depend/listen/keys/server.key',
                                                           f'{PROJECT_ROOT}/depend/listen/keys/server.crt'))

        reactor.run()
        print("HTTPS 协议监听模块已开启 443 port starting listen ...")
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()
