# 导入twisted的相关模块
import os
import re
import sys
import fnmatch
import django
from itertools import cycle

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__) + "../../../../../")
sys.path.append(PROJECT_ROOT)
os.environ['DJANGO_SETTINGS_MODULE'] = 'antenna.settings'
django.setup()

from twisted.internet import reactor
from twisted.names import dns, server
from utils.helper import send_message, send_email_message
from modules.message.constants import MESSAGE_TYPES
from modules.config.models import DnsConfig
from modules.message.models import Message
from modules.task.models import TaskConfig, TaskConfigItem
from modules.template.depend.base import BaseTemplate


# 创建一个DNS协议的处理类，继承自twisted.names.dns.DNSDatagramProtocol
class DNS(dns.DNSDatagramProtocol):
    def __init__(self, controller, reactor=None):
        super().__init__(controller, reactor)
        # 初始化变量
        self.dns_config = {}
        dns_recoed = DnsConfig.objects.all()
        self.dns_config_domain = [_dns.domain for _dns in dns_recoed]
        for _dns in dns_recoed:
            self.dns_config[_dns.domain] = cycle(_dns.value)

    # 重写datagramReceived方法，用来接收和处理DNS报文
    def datagramReceived(self, data, addr):
        # 使用twisted.names.dns.Message类来解析DNS报文
        try:
            message = dns.Message()
            message.fromStr(data)
            # 获取查询的域名和类型
            query = message.queries[0]
            name = query.name.name
            _type = query.type
            # 根据自己的逻辑返回相应的结果，例如IP地址或错误码
            self.dns_config_domain.sort(key=lambda x: x.startswith("*"))  # 进行排序
            print(addr[0], name.decode("utf-8"), flush=True)
            for domain in self.dns_config_domain:
                if fnmatch.fnmatch(name.decode("utf-8"), domain) and _type == dns.A:
                    # 创建一个回复的报文
                    reply = dns.RRHeader(name=name, type=dns.A, payload=dns.Record_A(
                        address=bytes(next(self.dns_config[domain]), encoding="utf-8")))
                    # 把回复的报文添加到答案部分
                    message.answers.append(reply)
                    # 设置响应码为0，表示成功
                    message.rCode = 0
                    # 存储数据
                    udomain = re.findall(r'\.?([^\.]+)\.%s' % domain.strip("*."), name.decode("utf-8"))
                    if udomain:
                        print(udomain[0], flush=True)
                        task_config_item = TaskConfigItem.objects.filter(task_config__key__iexact=udomain[0],
                                                                         task__status=1).first()
                        if task_config_item and task_config_item.template.name == "DNS":
                            username = task_config_item.task.user.username
                            Message.objects.create(domain=name.decode("utf-8"), message_type=MESSAGE_TYPES.DNS,
                                                   remote_addr=addr[0],
                                                   task_id=task_config_item.task_id,
                                                   template_id=task_config_item.template_id)
                            send_email_message(username, addr[0])
                            send_message(url=name.decode("utf-8"), remote_addr=addr[0], uri='', header='',
                                         message_type=MESSAGE_TYPES.DNS, content='', task_id=task_config_item.task_id)
                    break
                else:
                    # 设置响应码为3，表示域名不存在
                    message.rCode = 3
            # 把回复的报文转换为字节串
            data = message.toStr()
            # 把回复的报文发送给客户端
        except Exception as e:
            print("dns error", repr(e), flush=True)
        finally:
            self.transport.write(data, addr)


class DnsTemplate(BaseTemplate):
    info = [{
        "template_info": {
            "name": "DNS",  # 组件名
            "title": "DNS协议监听组件",  # 组件展示标题名
            "author": "bios000",  # 组件作者
            "type": 1,  # 组件类型，1是监听0是利用
            "desc": "",  # 组件介绍
            "desc_url": "",  # 组件使用说明链接
            "choice_type": 0,  # 组件选择类型0是单选，1是多选
            "payload": "{key}.{dns_domain}",  # 组件利用实例
            "file_name": "dnslog.py",

        },
        "item_info": [{
            "name": "dns_log",
            "config": [],

        }]}]

    def __init__(self):
        super().__init__()


def main():
    reactor.listenUDP(53, DNS(controller=server.DNSServerFactory))
    # 使用twisted.internet.reactor.run方法，运行事件循环，等待客户端的请求
    reactor.run()


if __name__ == '__main__':
    main()
