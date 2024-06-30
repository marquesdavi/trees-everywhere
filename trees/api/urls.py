from rest_framework.routers import DefaultRouter
from .views import PlantedTreeViewSet

router = DefaultRouter()
router.register(r"planted-trees", PlantedTreeViewSet, basename="plantedtree")

urlpatterns = router.urls
