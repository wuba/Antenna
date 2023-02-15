from rest_framework.routers import DefaultRouter

from modules.config.views import ConfigViewSet, DnsConfigViewSet
urlpatterns = [

]
router = DefaultRouter()
router.register(r'manage', ConfigViewSet, basename='manage')
router.register(r'dns', DnsConfigViewSet, basename='dns')
urlpatterns = router.urls + urlpatterns
