import binascii
import os
import socket
import sys

import django

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__) + "../../../../../")
sys.path.append(PROJECT_ROOT)
os.environ['DJANGO_SETTINGS_MODULE'] = 'antenna.settings'
django.setup()

from modules.config import setting
from modules.message.models import Message
from modules.task.models import Task, TaskConfig
from modules.template.depend.base import BaseTemplate
from modules.message.constants import MESSAGE_TYPES
from utils.helper import send_message, send_email_message


class SocketTemplate(BaseTemplate):
    info = [{
        "template_info": {
            "name": "LDAP",  # 组件名
            "title": "ldap协议监听组件",  # 组件展示标题名
            "author": "bios000",  # 组件作者
            "type": 1,  # 组件类型，1是监听0是利用
            "desc": "",  # 组件介绍
            "desc_url": "",  # 组件使用说明链接
            "choice_type": 0,  # 组件选择类型0是单选，1是多选
            "payload": "ldap://{domain}:{jndi_port}/{key}",
            "file_name": "jndi.py"
        },
        "item_info": [{
            "name": "ldap_log",
            "config": [],

        }]}, {
        "template_info": {
            "name": "RMI",  # 组件名
            "title": "rmi协议监听组件",  # 组件展示标题名
            "author": "bios000",  # 组件作者
            "type": 1,  # 组件类型，1是监听0是利用
            "desc": "",  # 组件介绍
            "desc_url": "",  # 组件使用说明链接
            "choice_type": 0,  # 组件选择类型0是单选，1是多选
            "payload": "rmi://{domain}:{jndi_port}/{key}",
            "file_name": "jndi.py"
        },
        "item_info": [{
            "name": "rmi_log",
            "config": [],

        }]}, ]

    def __init__(self):
        super().__init__()
        self.ss = None
        self.port = None

    def check_rmi(self, data):
        # 4a524d4900024b JMRI..K  判断rmi协议
        hex_data = binascii.hexlify(data).decode("utf-8")
        if hex_data[0:10] == '4a524d4900':
            if hex_data[10:12] != '01' and hex_data[10:12] != '02':
                return False
            if hex_data[12:] != '4b' and hex_data[12:] != '4c' and hex_data[12:] != '4d':
                return False
            return True
        return False

    def domessage(self, coon, addr):
        try:
            coon.settimeout(50)
            data = coon.recv(1024)
            # ldap协议
            hex_data = binascii.hexlify(data).decode("utf-8")
            if hex_data == "300c020101600702010304008000":
                send_data = b'\x30\x0c\x02\x01\x01\x61\x07\x0a\x01\x00\x04\x00\x04\x00'
                coon.send(send_data)
                data_2 = coon.recv(1024)
                length = int(data_2[8])
                remote_addr = addr[0]
                path = data_2[9:9 + length].decode()
                task_config_record = TaskConfig.objects.get(key=path)
                if task_config_record:
                    task_id = task_config_record.task_id
                    username = task_config_record.task.user.username
                    send_email_message(username, remote_addr)
                    Message.objects.create(domain=self.domain + "/" + self.key, remote_addr=remote_addr, uri=path,
                                           message_type=MESSAGE_TYPES.LDAP, task_id=task_id, template_id=10)
                    send_message(url=self.domain, remote_addr=remote_addr, uri=path, header='',
                                 message_type=MESSAGE_TYPES.LDAP, content='', task_id=task_id)
                coon.close()
            # rmi协议
            if self.check_rmi(data):
                send_data = b'\x4e\x00\x09\x31\x32\x37\x2e\x30\x2e\x30\x2e\x31\x00\x00\xc4\x12'
                coon.send(send_data)
                coon.recv(1024)
                coon.send(b'')
                path = coon.recv(1024)[-4:].decode()  # 平台key为4位
                remote_addr = addr[0]
                task_config_record = TaskConfig.objects.get(key=path)
                if task_config_record:
                    username = task_config_record.task.user.username
                    send_email_message(username, remote_addr)
                    task_id = task_config_record.task_id
                    Message.objects.create(domain=self.domain + "/" + self.key, remote_addr=remote_addr, uri=path,
                                           message_type=MESSAGE_TYPES.RMI, task_id=task_id, template_id=10)
                    send_message(url=self.domain, remote_addr=remote_addr, uri=path, header='',
                                 message_type=MESSAGE_TYPES.RMI, content='', task_id=task_id)
                coon.close()

        except Exception as e:
            print(e)
            coon.close()
            return

    def start(self, ip, port):
        try:
            self.port = port
            self.ip = ip
            self.ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print(f"开始监听地址：{self.ip}:{self.port}")
            self.ss.bind((self.ip, self.port))
            self.ss.listen(200)
            while True:
                coon, addr = self.ss.accept()
                self.domessage(coon, addr)
        except Exception as e:
            print(e)
            return


def main():
    jndi_server = SocketTemplate()
    jndi_server.start("0.0.0.0", 2345)


if __name__ == "__main__":
    main()
