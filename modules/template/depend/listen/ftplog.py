import os
import sys

import django
from twisted.internet import reactor
from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__) + "../../../../../")
sys.path.append(PROJECT_ROOT)
os.environ['DJANGO_SETTINGS_MODULE'] = 'antenna.settings'
django.setup()

from modules.message.constants import MESSAGE_TYPES
from modules.template.depend.base import *
from modules.config import setting

WELCOME_MSG = b'220 (vsFTPd 2.0.5) '
GOODBYE_MSG = b'221 Goodbye.'
USER_OK_NEED_PASS = b'331 Please specify the password.'
PLEASE_LOGIN = b'530 Please login with USER and PASS.'
LOGIN_WITH_USER_FIRST = b'503 Login with USER first.'
LOGIN_SUCCESS = b'230 Login success.'


class Ftp(LineReceiver):

    def __init__(self):
        self.file = ""
        self.password = None
        self.key = None
        self.remote_addr = None
        self.file_name = None
        self.content = {}
        self.state = 'get_name'

    def connectionMade(self):
        self.sendLine(WELCOME_MSG)
        self.remote_addr = self.transport.getPeer().host

    def connectionLost(self, line):
        self.sendLine(GOODBYE_MSG)
        flag, task_config_item = hit(self.key, template_name=["FTP", "XXE"], iexact=False)
        if flag:
            message_callback(domain=setting.PLATFORM_DOMAIN, remote_addr=self.remote_addr,
                             task_config_item=task_config_item, uri='', header='', message_type=MESSAGE_TYPES.FTP,
                             content=self.content)

    def lineReceived(self, line):
        if self.state == 'get_name':
            self.key = str(line, encoding="utf-8").replace("USER ", "")
            self.state = 'get_pass'
            self.sendLine(USER_OK_NEED_PASS)
        elif self.state == 'get_pass':
            if b"PASS " in line:
                self.password = str(line, encoding="utf-8").replace("PASS ", "")
                self.content = {"username": self.key, "password": self.password, }
                self.sendLine(b'230 Login success.')
            elif b"RETR " in line:
                content = str(line, encoding="utf-8").replace("RETR ", "")
                self.content["content"] = content
                self.sendLine(b'230 Login success.')
            elif b"EPSV" in line:
                self.sendLine(b'229 Entering exented')
            elif b"EPRT" in line:
                self.sendLine(b'200 PORT command ok')
            elif b"CWD " in line:
                self.file = str(self.file) + "/" + str(line, encoding="utf-8").replace("CWD ", "")
                self.content["cwd"] = self.file
                self.sendLine(b"250 antent is the current directory.!")
            else:
                self.sendLine(b'230 Login success.')


class FtpFactory(Factory):
    def buildProtocol(self, addr):
        return Ftp()


class FtpTemplate(BaseTemplate):
    info = [{
        "template_info": {
            "name": "FTP",  # 组件名
            "title": "FTP协议监听组件",  # 组件展示标题名
            "author": "bios000",  # 组件作者
            "type": 1,  # 组件类型，1是监听0是利用
            "desc": "",  # 组件介绍
            "desc_url": "",  # 组件使用说明链接
            "choice_type": 0,  # 组件选择类型0是单选，1是多选
            "payload": "ftp://{key}:123@{domain}/antenna",
            "file_name": "ftplog.py",
        },
        "item_info": [{
            "name": "ftp_log",
            "config": [],

        }]}]

    def __init__(self):
        super().__init__()


def main():
    try:
        reactor.listenTCP(21, FtpFactory())
        print("FTP 协议监听模块已开启 21 port starting listen ...")
        reactor.run()
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
