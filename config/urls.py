from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HomeView
from trees.api.viewsets import PlantedTreeViewSet

router = DefaultRouter()
router.register(r"planted-trees", PlantedTreeViewSet, basename="planted-tree")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", HomeView.as_view(), name="home"),
    path("accounts/", include("accounts.urls")),
    path("profiles/", include("profiles.urls")),
    path("trees/", include("trees.urls")),
    path("users/", include("users.urls")),
    path("api/", include(router.urls)),
    path("api/accounts/", include("accounts.api.urls", namespace="api")),
    path("accounts/", include("django.contrib.auth.urls")),
]
