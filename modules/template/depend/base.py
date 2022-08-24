from abc import abstractmethod
from modules.config.setting import SERVER_IP, PLATFORM_DOMAIN
from modules.task.models import TaskConfigItem


class BaseTemplate:
    template_info = {
        "name": "",  # 组件名
        "title": "",  # 组件展示标题名
        "author": "",  # 组件作者
        "type": 1,  # 组件类型
        "desc": "",  # 组件介绍
        "desc_url": "",  # 组件使用说明链接
        "choice_type": 1,  # 组件选择类型
        "url_type": 1,  # 组件生成链接格式类型
    }

    def __init__(self):
        self.ip = SERVER_IP
        self.domain = PLATFORM_DOMAIN

    def run(self, key):
        task_config_item = TaskConfigItem.objects.filter(task_config__key=key)
        if task_config_item:
            config = [{"name": i.template_config_item.name, "config": i.value,}
                      for i in
                      task_config_item]
        else:
            config = []
        return self.generate(key, config)

    @abstractmethod
    def generate(self, key, config):
        pass
