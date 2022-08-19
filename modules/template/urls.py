from django.urls import path
from rest_framework.routers import DefaultRouter

from modules.template.views import TemplateViewSet, TemplateConfigItemViewSet

urlpatterns = [

]

router = DefaultRouter()

router.register(r'manage', TemplateViewSet, basename='templates')
router.register(r'configs', TemplateConfigItemViewSet, basename='template_config_iterm')

urlpatterns = router.urls + urlpatterns
