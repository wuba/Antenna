from modules.message import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
urlpatterns = [
]
router.register(r'manage', views.MessageView)
urlpatterns += router.urls
