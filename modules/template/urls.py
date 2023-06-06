from django.urls import path
from rest_framework.routers import DefaultRouter

from modules.template.views import TemplateViewSet, TemplateConfigItemViewSet,UrlTemplateViewSet

urlpatterns = [

]

router = DefaultRouter()

router.register(r'manage', TemplateViewSet, basename='templates')
router.register(r'configs', TemplateConfigItemViewSet, basename='template_config_iterm')
router.register(r'url', UrlTemplateViewSet, basename='url_templates')

urlpatterns = router.urls + urlpatterns
