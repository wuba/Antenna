import base64
import hashlib
import json
import os
import random
import smtplib
import socket
import string
import time
from email.mime.text import MIMEText
from functools import wraps

from django.conf import settings
import requests
from django_filters.filters import Filter
from modules.config.models import Config
from modules.template.models import Template
from rest_framework import status
from rest_framework.response import Response
from modules.task.models import Task, TaskConfig
from modules.config.setting import JNDI_PORT, PLATFORM_DOMAIN


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
    mailserver = Config.objects.get(name="EMAIL_HOST").value  # 邮箱服务器地址
    port = int(Config.objects.get(name="EMAIL_PORT").value)
    username_send = Config.objects.get(name="EMAIL_HOST_USER").value  # 邮箱用户名
    password = Config.objects.get(name="EMAIL_HOST_PASSWORD").value  # 邮箱密码：需要使用授权码
    username_recv = "".join(to)  # 收件人，多个收件人用逗号隔开
    mail = MIMEText(message)
    mail['Subject'] = 'Antenna平台邮件'
    mail['From'] = username_send
    mail['To'] = username_recv
    if port == 25:
        smtp = smtplib.SMTP(mailserver, port=port)
    else:
        smtp = smtplib.SMTP_SSL(mailserver, port=port)  # QQ邮箱的服务器和端口号
    smtp.login(username_send, password)  # 登录邮箱
    smtp.sendmail(username_send, username_recv, mail.as_string())  # 参数分别是发送者，接收者，第三个是把上面的发送邮件的内容变成字符串
    smtp.quit()  # 发送完毕后退出smtp
    return True


def get_result_data(data):
    """
    修改任务详情接口返回格式
    """
    if not data:
        return Response(data={}, status=status.HTTP_200_OK)
    listen_data_list = []
    payload_data_list = []
    for i in data:
        task_config_status = 1
        task_config_id = i["task_config"]
        template_id = i["template"]
        task_id = i["task"]
        task_config_item_id = i["id"]
        template_config_item_id = i["template_config_item"]
        value = i["value"]
        key = TaskConfig.objects.get(id=task_config_id).key
        template_record = Template.objects.get(id=template_id)
        url = get_payload(key, template_record.payload)
        for _data_old in payload_data_list:
            if task_config_id == _data_old.get("task_config_id", 0):
                _data_old["task_config_item_list"].append({
                    "template_config_item": template_config_item_id,
                    "id": task_config_item_id,
                    "value": value})
                task_config_status = 0
        if task_config_status:
            _data = {
                "task": task_id,
                "template": template_id,
                "template_name": template_record.name,
                "template_type": template_record.type,
                "template_choice_type": template_record.choice_type,
                "task_config_id": task_config_id,
                "key": url,
                "task_config_item_list": [{
                    "template_config_item": template_config_item_id,
                    "id": task_config_item_id,
                    "value": value}]
            }

            if template_record.type == 1:
                listen_data_list.append(_data)
            else:
                payload_data_list.append(_data)
    task_record = Task.objects.get(id=int(data[0]["task"]))
    result = {
        "task_info": {
            "task_id": task_id,
            "task_name": task_record.name,
            "callback_url": task_record.callback_url,
            "callback_url_headers": task_record.callback_url_headers,
            "show_dashboard": bool(task_record.show_dashboard)},
        "listen_template_info": listen_data_list,
        "payload_template_info": payload_data_list,
    }
    return Response(result, status=status.HTTP_200_OK)


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
        shell_path = os.path.abspath(os.path.dirname(__file__) + "/../bin/run.sh")
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
            response = requests.post(url=message_url, json=data, headers=message_headers, timeout=3)
            print("发送请求")
    except Exception as e:
        print(e)
        pass
