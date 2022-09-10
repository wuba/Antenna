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
    domain_in = django_filters.CharFilter(field_name='domain', method='get_domain_in')

    def get_domain_in(self, queryset, name, value):
        a = value.replace("[", "").replace("]", "").split(",")
        b = [b.replace("\"", "").replace("'", "") for b in a]
        return queryset.filter(domain__in=b)

    class Meta:
        model = Message
        fields = "__all__"
