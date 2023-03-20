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
    domain_in = django_filters.CharFilter(field_name='domain', lookup_expr='in')
    content_contains = django_filters.CharFilter(field_name='content', lookup_expr='icontains')
    domain_contains = django_filters.CharFilter(field_name='domain', lookup_expr='icontains')
    order_desc = django_filters.CharFilter(method='order_by_desc', initial='desc')
    task_name = django_filters.CharFilter(field_name='task__name')
    message_type = django_filters.NumberFilter(field_name='message_type')
    template_name = django_filters.CharFilter(field_name='template__name')
    task = django_filters.NumberFilter(field_name='task')
    content = django_filters.CharFilter(field_name='content')
    create_time = django_filters.DateFilter(field_name="create_time")
    def order_by_desc(self, queryset, name, value):
        if value == "asc":
            return queryset.order_by('create_time')
        return queryset.order_by('-create_time')

    class Meta:
        model = Message
        fields = "__all__"
