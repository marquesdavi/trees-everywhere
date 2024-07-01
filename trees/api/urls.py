from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PlantedTreeViewSet

router = DefaultRouter()
router.register(r"planted-trees", PlantedTreeViewSet, basename="plantedtree")

#app_name = "trees"

urlpatterns = [
    path("", include(router.urls)),
]




