from django.contrib import admin
from django.urls import path, include
from .views import HomeView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", HomeView.as_view(), name="home"),
    path("accounts/", include("accounts.urls")),
    path("profiles/", include("profiles.urls")),
    path("users/", include("users.urls")),
    path("trees/", include("trees.urls")),
    path(
        "api/trees/", include("trees.api.urls")
    ), 
    path("api/accounts/", include("accounts.api.urls", namespace="api")),
    path("accounts/", include("django.contrib.auth.urls")),
]
