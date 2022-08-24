from rest_framework.routers import DefaultRouter
from modules.task.views import TaskInfoViewSet, TaskConfigItemViewSet

urlpatterns = [

]

router = DefaultRouter()
router.register(r'configs', TaskConfigItemViewSet, basename='task_config_item')
router.register(r'manage', TaskInfoViewSet, basename='tasks')
urlpatterns = router.urls + urlpatterns
