import os
import sys
from urllib.parse import urlparse, parse_qs

from twisted.internet import reactor, ssl
from twisted.web.client import HTTPConnectionPool, Agent
from twisted.web.server import Site, NOT_DONE_YET
from twisted.web.resource import Resource
from twisted.internet.protocol import Protocol, ClientFactory
from twisted.web.http import RESPONSES as Response
import django
from io import BytesIO
from twisted.web.client import FileBodyProducer
from twisted.internet.defer import succeed

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__) + "../../../../../")
sys.path.append(PROJECT_ROOT)
os.environ['DJANGO_SETTINGS_MODULE'] = 'antenna.settings'

django.setup()

from modules.message.constants import MESSAGE_TYPES
from modules.message.models import Message
from modules.task.models import TaskConfigItem
from utils.helper import send_email_message, send_message


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
        print(f"Full HTTP request:\n{self.html}")

        parsed_uri = urlparse(request.uri.decode('utf-8'))
        query_params = parse_qs(parsed_uri.query)
        if 'message' in query_params:
            self.content = query_params['message'][0]

        task_config_item = TaskConfigItem.objects.filter(task_config__key=self.key, task__status=1).first()
        if task_config_item and task_config_item.template.name == "HTTPS":
            username = task_config_item.task.user.username
            send_email_message(username, self.remote_addr)
            Message.objects.create(domain=self.domain, message_type=MESSAGE_TYPES.HTTPS,
                                   remote_addr=self.remote_addr,
                                   task_id=task_config_item.task_id,
                                   uri=self.uri,
                                   template_id=task_config_item.template_id,
                                   content=self.content,
                                   html=self.html)
            send_message(url=self.domain, remote_addr=self.remote_addr, uri=self.uri, header='',
                         message_type=MESSAGE_TYPES.HTTPS, content=self.content,
                         task_id=task_config_item.task_id, raw=self.html)

        agent = Agent(reactor, pool=self.pool)
        body_producer = FileBodyProducer(request.content)
        d = agent.request(request.method, b'http://0.0.0.0:80' + request.uri,
                          request.requestHeaders, body_producer)
        d.addCallbacks(self.handle_response, self.handle_error, callbackArgs=(request,), errbackArgs=(request,))

        return NOT_DONE_YET

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


root = MyResource()

factory = Site(root)
reactor.listenSSL(443, factory,
                  ssl.DefaultOpenSSLContextFactory(f'{PROJECT_ROOT}/conf/server.key',
                                                   f'{PROJECT_ROOT}/conf/server.crt'))
reactor.run()
