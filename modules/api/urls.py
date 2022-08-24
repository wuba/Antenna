from rest_framework.routers import DefaultRouter

from modules.api.views import ApiKeyViewSet

urlpatterns = [

]
router = DefaultRouter()
router.register(r'key', ApiKeyViewSet, basename='apikey')
urlpatterns = router.urls + urlpatterns
