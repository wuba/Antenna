from datetime import datetime, timedelta

from modules.message.models import Message
from modules.config import setting


def delete_old_messages():
    """定时任务检测是否删除最近七天以外的数据"""
    if setting.SAVE_MESSAGE_SEVEN_DAYS == 1:
        print("开始检测")
        seven_days_ago = datetime.now() - timedelta(days=7)
        Message.objects.filter(created_at__lt=seven_days_ago).delete()
