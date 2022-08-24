from django.contrib.auth.models import User
from django.db import models


class ApiKey(models.Model):
    """
    用户apikey
    """
    key = models.CharField(max_length=32, help_text='apikey')
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_constraint=False, help_text="用户", null=True)
    update_time = models.DateTimeField(auto_now_add=True, null=True, blank=True, help_text="创建时间")

    class Meta:
        db_table = 'api_key'
