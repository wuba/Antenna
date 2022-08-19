from django.urls import path
from rest_framework.routers import DefaultRouter

from modules.account.views import EmailCodeViewSet, UserViewSet

urlpatterns = [

]

router = DefaultRouter()
router.register(r'sendmail', EmailCodeViewSet, basename='sendmail')
router.register(r'user', UserViewSet, basename='user')

urlpatterns = router.urls + urlpatterns

