from rest_framework.routers import DefaultRouter

from modules.config.views import ConfigViewSet
urlpatterns = [

]
router = DefaultRouter()
router.register(r'manage', ConfigViewSet, basename='manage')
urlpatterns = router.urls + urlpatterns



