import django_filters
from rest_framework import serializers
from modules.message.models import Message


class MessageSerializer(serializers.ModelSerializer):
    task_name = serializers.CharField(source='task.name', read_only=True)

    class Meta:
        model = Message
        fields = "__all__"


class MessageFilter(django_filters.FilterSet):
    month = django_filters.NumberFilter(field_name='create_time', lookup_expr='month')
    year = django_filters.NumberFilter(field_name='create_time', lookup_expr='year')

    class Meta:
        model = Message
        fields = "__all__"
