import copy
import os
import re
import sys
import tempfile

import django
from dnslib import QTYPE, RCODE, RR, TXT
from dnslib.server import BaseResolver, DNSServer

from modules.message.constants import MESSAGE_TYPES
from utils.helper import send_message

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__) + "../../../")
sys.path.append(PROJECT_ROOT)
os.environ['DJANGO_SETTINGS_MODULE'] = 'antenna.settings'
django.setup()

from modules.config.setting import DNS_DOMAIN, DNS_PORT, NS1_DOMAIN, NS2_DOMAIN, SERVER_IP
from modules.message.models import Message
from modules.task.models import TaskConfig, TaskConfigItem
from modules.template.depend.base import BaseTemplate


class MysqlLogger():
    def log_data(self, dnsobj):
        pass

    def log_error(self, handler, e):
        pass

    def log_pass(self, *args):
        pass

    def log_prefix(self, handler):
        pass

    def log_recv(self, handler, data):
        pass

    def log_reply(self, handler, reply):
        pass

    def log_request(self, handler, request):
        domain = request.q.qname.__str__()
        print('domain=======>', domain)
        if domain.endswith(DNS_DOMAIN + '.'):
            udomain = re.search(r'\.?([^\.]+)\.%s\.' % DNS_DOMAIN, domain)
            print('udomain=======>', udomain)
            if udomain:
                print("udomain.group(1))======>", udomain.group(1))
                domain_key = udomain.group(1)
                task_config_item = TaskConfigItem.objects.filter(task_config__key__icontains=domain_key,
                                                                 task__status=1).first()
                if task_config_item and task_config_item.template.name == "DNS":
                    domain = domain.strip(".")
                    Message.objects.create(domain=domain, message_type=MESSAGE_TYPES.DNS,
                                           remote_addr=handler.client_address[0],
                                           task_id=task_config_item.task_id, template_id=task_config_item.template_id)
                    send_message(url=domain, remote_addr=handler.client_address[0], uri='', header='',
                                 message_type=MESSAGE_TYPES.DNS, content='', task_id=task_config_item.task_id)

    def log_send(self, handler, data):
        pass

    def log_truncated(self, handler, reply):
        pass


class ZoneResolver(BaseResolver):
    """
        Simple fixed zone file resolver.
    """

    def __init__(self, zone, glob=False):
        """
            Initialise resolver from zone file.
            Stores RRs as a list of (label,type,rr) tuples
            If 'glob' is True use glob match against zone file
        """
        self.zone = [(rr.rname, QTYPE[rr.rtype], rr)
                     for rr in RR.fromZone(zone)]
        self.glob = glob
        self.eq = 'matchGlob' if glob else '__eq__'

    def resolve(self, request, handler):
        """
            Respond to DNS request - parameters are request packet & handler.
            Method is expected to return DNS response
        """
        reply = request.reply()
        qname = request.q.qname
        qtype = QTYPE[request.q.qtype]
        if qtype == 'TXT':
            txtpath = os.path.join(tempfile.gettempdir(), str(qname).lower())
            if os.path.isfile(txtpath):
                reply.add_answer(
                    RR(qname, QTYPE.TXT, rdata=TXT(open(txtpath).read().strip())))
        for name, rtype, rr in self.zone:
            # Check if label & type match
            if getattr(qname, self.eq)(name) and (qtype == rtype or qtype == 'ANY'
                                                  or rtype == 'CNAME'):
                # If we have a glob match fix reply label
                if self.glob:
                    a = copy.copy(rr)
                    a.rname = qname
                    reply.add_answer(a)
                else:
                    reply.add_answer(rr)
                # Check for A/AAAA records associated with reply and
                # add in additional section
                if rtype in ['CNAME', 'NS', 'MX', 'PTR']:
                    for a_name, a_rtype, a_rr in self.zone:
                        if a_name == rr.rdata.label and a_rtype in [
                            'A', 'AAAA'
                        ]:
                            reply.add_ar(a_rr)
        if not reply.rr:
            reply.header.rcode = RCODE.NXDOMAIN
        print('reply======>', reply)
        return reply


def main():
    zone = '''
*.{dnsdomain}.       IN      NS      {ns1domain}.
*.{dnsdomain}.       IN      NS      {ns2domain}.
*.{dnsdomain}.       IN      A       {serverip}
{dnsdomain}.         IN      A       {serverip}
'''.format(
        dnsdomain=DNS_DOMAIN,
        ns1domain=NS1_DOMAIN,
        ns2domain=NS2_DOMAIN,
        serverip=SERVER_IP)
    resolver = ZoneResolver(zone, True)
    print("当前DNS解析表:\r\n" + zone)
    logger = MysqlLogger()
    print("Starting Zone Resolver (%s:%d) [%s]" % ("*", DNS_PORT, "UDP"))
    udp_server = DNSServer(resolver, port=53, address="0.0.0.0", logger=logger)
    udp_server.start()


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


if __name__ == '__main__':
    main()
