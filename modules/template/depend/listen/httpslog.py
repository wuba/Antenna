import os
import sys
import django
from urllib.parse import urlparse, parse_qs
from twisted.internet import reactor, ssl
from twisted.web.client import HTTPConnectionPool, Agent
from twisted.web.server import Site, NOT_DONE_YET
from twisted.web.resource import Resource
from twisted.internet.protocol import Protocol, ClientFactory

from twisted.web.client import FileBodyProducer

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__) + "../../../../../")
sys.path.append(PROJECT_ROOT)
os.environ['DJANGO_SETTINGS_MODULE'] = 'antenna.settings'

django.setup()
from modules.template.depend.base import *


class MyResource(Resource):
    isLeaf = True

    def __init__(self):
        super().__init__()
        self.body = None
        self.content = None
        self.remote_addr = None
        self.uri = None
        self.key = None
        self.domain = None
        self.pool = HTTPConnectionPool(reactor)

    def render(self, request):
        try:
            self.remote_addr = request.getClientAddress().host
            domain = request.requestHeaders.getRawHeaders(b"host", [None])[0]
            if domain:
                self.domain = domain.decode('utf-8')
                self.key = self.domain.split('.')[0]
            self.uri = urlparse(request.uri.decode('utf-8')).path.strip("/")
            self.body = request.content.read().decode('utf-8')
            request.content.seek(0)
            # Extract request line
            request_line = f"{request.method.decode('utf-8')} {request.uri.decode('utf-8')} {request.clientproto.decode('utf-8')}"

            # Extract headers
            headers = ""
            for name, values in request.requestHeaders.getAllRawHeaders():
                for value in values:
                    headers += f"{name.decode('utf-8')}: {value.decode('utf-8')}\r\n"

            self.html = f"{request_line}\r\n{headers}\r\n{self.body}"

            parsed_uri = urlparse(request.uri.decode('utf-8'))
            query_params = parse_qs(parsed_uri.query)
            if 'message' in query_params:
                self.content = query_params['message'][0]

            if len(self.key) == 4 and self.key != setting.PLATFORM_DOMAIN.split('.')[0]:
                flag, task_config_item = hit(self.key, template_name=["HTTPS"], iexact=True)
                if flag:
                    message_callback(domain=self.domain, remote_addr=self.remote_addr,
                                     task_config_item=task_config_item,
                                     uri=self.uri, header='', message_type=MESSAGE_TYPES.HTTPS, content=self.content,
                                     raw=self.html)

            agent = Agent(reactor, pool=self.pool)
            body_producer = FileBodyProducer(request.content)
            d = agent.request(request.method, b'http://0.0.0.0:80' + request.uri,
                              request.requestHeaders, body_producer)
            d.addCallbacks(self.handle_response, self.handle_error, callbackArgs=(request,), errbackArgs=(request,))

            return NOT_DONE_YET
        except Exception as e:
            print(e)

    def handle_response(self, response, request):
        request.setResponseCode(response.code)
        for name, values in response.headers.getAllRawHeaders():
            request.responseHeaders.setRawHeaders(name, values)
        response.deliverBody(FinishedRequest(request))

    def handle_error(self, error, request):
        print(f"Error: {error}")
        request.setResponseCode(500)
        request.write(b"Internal Server Error")
        request.finish()


class FinishedRequest(Protocol):
    def __init__(self, request):
        self.request = request

    def dataReceived(self, data):
        self.request.write(data)

    def connectionLost(self, reason):
        self.request.finish()


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
        print(f"HTTPS 协议监听模块已开启 443 port starting listen ...", flush=True)
        root = MyResource()

        factory = Site(root)
        reactor.listenSSL(443, factory,
                          ssl.DefaultOpenSSLContextFactory(f'{PROJECT_ROOT}/conf/server.key',
                                                           f'{PROJECT_ROOT}/conf/server.crt'))
        reactor.run()
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()
