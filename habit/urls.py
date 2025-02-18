from rest_framework.routers import DefaultRouter

from .apps import HabitConfig
from .views import HabitViewSet

app_name = HabitConfig.name

router = DefaultRouter()
router.register("habits", HabitViewSet, basename="habits")

urlpatterns = router.urls
