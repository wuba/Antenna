from django.http import HttpResponse

from modules.template.depend.base import BaseTemplate
from modules.template.depend.payload import *
from modules.template.depend.listen import http, jndi, dnslog
from modules.template.models import Template, TemplateConfigItem


def match_template(item):
    """
    根据key判断所属模板，根据模板配置返回response
    """
    key = item.task_config.key
    template_name = item.template.name
    template_response = HttpResponse('', content_type='text/plain;charset=UTF-8')
    for c in BaseTemplate.__subclasses__():
        for info in c.info:
            if str(info["template_info"]["name"]) == str(template_name):
                template_response = c().run(key)
                break
    return template_response


def load_template(user_id):
    """
    加载刷新组件及其配置
    """
    for c in BaseTemplate.__subclasses__():
        for info in c.info:
            template = info["template_info"]
            template_object, create = Template.objects.update_or_create(defaults=template,
                                                                        name=template.get("name", ""), user_id=user_id)
            item = info["item_info"]
            for i in item:
                i["template_id"] = template_object.id
                TemplateConfigItem.objects.update_or_create(defaults=i, name=i.get("name", ""),
                                                            template__user_id=user_id)
