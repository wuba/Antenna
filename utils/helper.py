import base64
import hashlib
import json
import os
import random
import smtplib
import socket
import string
import subprocess
import sys
import time
from email.mime.text import MIMEText
from functools import wraps

import django
from modules.message.constants import MESSAGE_TYPES

from django.conf import settings
import requests
from django_filters.filters import Filter
from modules.task.models import Task, TaskConfig
from modules.config import setting


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
        if not TaskConfig.objects.filter(key__icontains=random_code).exists():
            break

    return random_code


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


def get_payload(task_config, payload):
    """
    转换地址，可选用关键字
    {domain} 平台域名
    {key}  任务key
    {jndi_port}  jndi端口
    {dns_domain}  dns域名
    """

    url = payload if not task_config.url_template_id else task_config.url_template.payload
    return url.replace("{domain}", setting.PLATFORM_DOMAIN).replace("{key}", task_config.key).replace(
        "{jndi_port}", str(setting.JNDI_PORT)).replace("{dns_domain}", setting.DNS_DOMAIN)


def send_mail(to, message):
    """
    发送邮件
    """
    try:
        if to == "antenna@58.com":
            return False
        mailserver = setting.EMAIL_HOST  # 邮箱服务器地址
        port = int(setting.EMAIL_PORT)
        username_send = setting.EMAIL_HOST_USER  # 邮箱用户名
        password = setting.EMAIL_HOST_PASSWORD  # 邮箱密码：需要使用授权码
        print(setting.EMAIL_HOST_USER, setting.EMAIL_HOST_PASSWORD)
        username_recv = "".join(to)  # 收件人，多个收件人用逗号隔开
        mail = MIMEText(message)
        mail['Subject'] = 'Antenna平台邮件'
        mail['From'] = username_send
        mail['To'] = username_recv
        smtp = None
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
        print("send email error", repr(e))
        return False


import time

SENT_TIME_MAP = {}  # 记录每个用户上次发送邮件的时间


def send_email_message(username, ip):
    """接收到消息发送给对应用户"""
    try:
        if setting.OPEN_EMAIL == 1:
            # 检查用户上次发送邮件的时间
            last_sent_time = SENT_TIME_MAP.get(username, 0)
            current_time = int(time.time())
            if current_time - last_sent_time < 60:
                # 如果距离上次发送邮件的时间不足 60 秒，则不发送本次邮件
                return
            else:
                # 更新用户上次发送邮件的时间
                SENT_TIME_MAP[username] = current_time

            # 发送邮件
            message = f"""【ANTENNA】平台接收到来自{ip}的请求,请查看"""
            send_mail(username, message)
    except Exception as e:
        print("send_email_message error", repr(e))


def is_base64(s):
    try:
        # 尝试解码字符串
        base64.decodebytes(s.encode('utf-8'))
        return base64.b64decode(s).decode('utf-8')
    except Exception:
        # 解码失败，说明不是 base64 编码的字符串，返回原内容
        return s


def restart():
    """重启服务"""
    try:
        shell_path = os.path.abspath(os.path.dirname(__file__) + "/../bin/docker_restart.sh")
        print(f"开始重启 {shell_path}")
        subprocess.Popen(['/bin/sh', shell_path], start_new_session=True)
    except Exception as e:
        print(e)


def send_message(url, remote_addr, uri, header, message_type, content, task_id, raw=""):
    """
    发送消息到接口
    """
    try:
        data = {
            "domain": url, "remote_addr": remote_addr, "uri": uri, "header": header,
            "message_type": message_type, "content": content, "raw": raw}
        task_record = Task.objects.get(id=task_id)
        if task_record.callback_url:
            message_url = task_record.callback_url
            message_headers = json.loads(task_record.callback_url_headers)
            if message_url and message_headers:
                requests.post(url=message_url, json=data, headers=message_headers, timeout=3)
                print("发送请求")
    except Exception as e:
        print(e)


def get_message_type_name(message_type):
    for MESSAGE_TYPE in MESSAGE_TYPES:
        if MESSAGE_TYPE[0] == message_type:
            return MESSAGE_TYPE[1]


def reconstruct_request(request):
    # 请求行
    request_line = '{method} {path} HTTP/1.1\r\n'.format(
        method=request.method,
        path=request.path
    )

    # 请求头
    headers = ''
    for name, value in request.headers.items():
        headers += '{name}: {value}\r\n'.format(name=name, value=value)

    # 请求体
    body = request.body.decode('utf-8')

    # 数据报文
    message = '{request_line}{headers}\r\n{body}'.format(
        request_line=request_line,
        headers=headers,
        body=body
    )
    return message


def get_param_message(request):
    """
    获取请求的参数以及message参数
    """
    if request.method == 'GET':
        params = request.GET.dict()
    elif request.method == 'POST':
        try:
            params = request.POST.dict()
        except Exception as e:
            print(f'Failed to get POST params: {e}')
            params = {}
    else:
        try:
            json_str = request.body.decode('utf-8')
            params = json.loads(json_str)
        except Exception as e:
            print(f'Failed to get JSON params: {e}')
            params = {}

    base64_message = params.get('message', '')
    message = is_base64(base64_message) if base64_message else ''
    return params, message


def get_lastest_verson():
    """
    获取github 最新版本
    """
    latest_version = ""
    response = requests.get(f"https://api.github.com/repos/wuba/antenna/releases")
    if response.status_code == 200:
        releases = response.json()
        latest_release = releases[0]  # 按时间顺序排列，最新版本在第一个位置
        latest_version = latest_release['tag_name']
        print(f"Latest version on GitHub: {latest_version}")

    return latest_version


