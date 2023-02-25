import os

from django.http import HttpResponse

from modules.template.constants import TEMPLATE_TYPES
from modules.template.depend.base import BaseTemplate
from modules.template.depend.payload import *
from modules.template.depend.listen import httplog, jndi, dnslog, ftplog, httpslog
from modules.template.models import Template, TemplateConfigItem


def match_template(item, param_list=None):
    """
    根据key判断所属模板，根据模板配置返回response
    """
    if param_list is None:
        param_list = {}
    key = item.task_config.key
    template_name = item.template.name
    template_response = HttpResponse('', content_type='text/plain;charset=UTF-8')
    for c in BaseTemplate.__subclasses__():
        if c.info:
            for info in c.info:
                if str(info["template_info"]["name"]) == str(template_name):
                    template_response = c().run(key, param_list)
                    break
        elif not c.info and c.__name__ == str(template_name):
            template_response = c().run(key, param_list)

    return template_response


def view_template_code(filename, template_type):
    """
    获取组件的代码
    """
    base_path = str(os.path.abspath(os.path.dirname(__file__)))
    # 读取文件内容
    if template_type == TEMPLATE_TYPES.PAYLOAD:
        file_path = base_path + f"/depend/payload/{filename}"
    else:
        file_path = base_path + f"/depend/listen/{filename}"
    file_object = open(file_path, 'r')
    try:
        code = file_object.read()  # 结果为str类型
    finally:
        file_object.close()
    return code


def load_template():
    """
    加载刷新组件及其配置
    """
    for c in BaseTemplate.__subclasses__():
        if not c.info:
            continue
        for info in c.info:
            template = info.get("template_info", "")
            template["code"] = view_template_code(filename=template.get("file_name", ""),
                                                  template_type=template.get("type", 1))
            template_record = Template.objects.update_or_create(template, name=template.get("name", ""))
            item = info.get("item_info", "")
            for i in item:
                i["template_id"] = template_record[0].id
                TemplateConfigItem.objects.update_or_create(i, name=i.get("name", ""))
