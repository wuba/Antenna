from rest_framework import serializers
from modules.api.models import ApiKey


class ApiKeySerializer(serializers.ModelSerializer):
    """
    api序列化器
    """

    class Meta:
        model = ApiKey
        fields = ('key',)
