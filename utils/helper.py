import base64
import hashlib
import json
import os
import random
import smtplib
import socket
import string
import sys
import time
from email.mime.text import MIMEText
from functools import wraps

import django

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__) + "../../../")
sys.path.append(PROJECT_ROOT)
os.environ['DJANGO_SETTINGS_MODULE'] = 'antenna.settings'
django.setup()

from django.conf import settings
import requests
from django_filters.filters import Filter
from modules.task.models import Task, TaskConfig
from modules.config.setting import JNDI_PORT, PLATFORM_DOMAIN, EMAIL_HOST, EMAIL_PORT, EMAIL_HOST_USER, \
    EMAIL_HOST_PASSWORD


def get_host_ip():
    """ 获取本机IP """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((settings.DNS_SERVER, 80))
        ip = s.getsockname()[0]
    except Exception as e:
        ip = ""
    finally:
        s.close()
    return ip


def env(name):
    '''
    环境变量拦截器
    '''

    def decorate(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if name == os.environ.get("WCloud_Env"):
                return func(*args, **kwargs)

        return wrapper

    return decorate


class ListFilter(Filter):
    def __init__(self, query_param, *args, **kwargs):
        super(ListFilter, self).__init__(*args, **kwargs)
        self.query_param = query_param
        self.lookup_expr = 'in'

    def filter(self, queryset, value):
        try:
            request = self.parent.request
        except AttributeError:
            return None

        values = request.GET.getlist(self.query_param)
        values = [int(item) if item.isdigit() else item for item in list(set(values))]
        return super(ListFilter, self).filter(queryset, values)


def create_salt(length=6):
    """Generate a random string of letters and digits """
    letters_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_digits) for i in range(length))


def create_md5(txt):
    return hashlib.md5(txt.encode('utf-8')).hexdigest()


def token_generate(content, salt=None):
    token_str = str(content) + str(time.time()) + (salt if salt else create_salt())
    md5_str = create_md5(token_str)
    return md5_str.lower()


def generate_code(number):
    """
    生成验证码
    :return:
    """
    while True:
        random_code = ''.join(random.sample(string.ascii_letters + string.digits, number))
        if not TaskConfig.objects.filter(key=random_code).exists():
            break

    return random_code


def create_salt(length=6):
    """Generate a random string of letters and digits """
    letters_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_digits) for i in range(length))


def create_md5(txt):
    return hashlib.md5(txt.encode('utf-8')).hexdigest()


def token_generate(content, salt=None):
    token_str = str(content) + str(time.time()) + (salt if salt else create_salt())
    md5_str = create_md5(token_str)
    return md5_str.lower()


def convert(data):
    if isinstance(data, bytes):
        return data.decode()
    if isinstance(data, dict):
        return dict(map(convert, data.items()))
    if isinstance(data, tuple):
        return tuple(map(convert, data))
    if isinstance(data, list):
        return list(map(convert, data))
    return data


def get_payload(key, payload):
    """
    获取地址
    """

    return payload.replace("{domain}", PLATFORM_DOMAIN).replace("{key}", key).replace("{jndi_port}", str(JNDI_PORT))


def send_mail(to, message):
    """
    发送邮件
    """
    try:
        mailserver = EMAIL_HOST  # 邮箱服务器地址
        port = int(EMAIL_PORT)
        username_send = EMAIL_HOST_USER  # 邮箱用户名
        password = EMAIL_HOST_PASSWORD  # 邮箱密码：需要使用授权码
        username_recv = "".join(to)  # 收件人，多个收件人用逗号隔开
        mail = MIMEText(message)
        mail['Subject'] = 'Antenna平台邮件'
        mail['From'] = username_send
        mail['To'] = username_recv
        if port == 25 or port == 587:
            smtp = smtplib.SMTP(mailserver, port=port)
            smtp.starttls()
        elif port == 465:
            smtp = smtplib.SMTP_SSL(mailserver, port=port)  # QQ邮箱的服务器和端口号
        smtp.login(username_send, password)  # 登录邮箱
        smtp.sendmail(username_send, username_recv, mail.as_string())  # 参数分别是发送者，接收者，第三个是把上面的发送邮件的内容变成字符串
        smtp.quit()  # 发送完毕后退出smtp
        return True

    except Exception as e:
        print(e)
        return False


def is_base64(content):
    """
    判断内容是否base64编码
    """
    content = content.replace(' ', '+')
    if len(content) % 4 != 0:
        return content
    for i in content:
        if ('a' <= i <= 'z') or ('A' <= i <= 'Z') or ('0' <= i <= '9') or i == '+' or i == '/' or i == '=':
            pass
        else:
            return content
    return str(base64.b64decode(content), 'utf-8')


def restart():
    try:
        shell_path = os.path.abspath(os.path.dirname(__file__) + "/../bin/restart.sh")
        print(f"开始重启 {shell_path}")
        os.system(f"sh {shell_path}")
    except Exception as e:
        print(e)


def send_message(url, remote_addr, uri, header, message_type, content, task_id):
    """
    发送消息到接口
    """
    try:
        data = {
            "domain": url, "remote_addr": remote_addr, "uri": uri, "header": header,
            "message_type": message_type, "content": content}
        task_record = Task.objects.get(id=task_id)
        message_url = task_record.callback_url
        message_headers = json.loads(task_record.callback_url_headers)
        if message_url and message_headers:
            requests.post(url=message_url, json=data, headers=message_headers, timeout=3)
            print("发送请求")
    except Exception as e:
        print(e)

