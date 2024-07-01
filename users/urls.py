from django.urls import path
from .views import (
    UserRegistrationView,
    UserLoginView,
    UserLogoutView,
    ProfileDetailView,
    ProfileUpdateView,
)

urlpatterns = [
    path("signup/", UserRegistrationView.as_view(), name="signup"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
    path("profile/", ProfileDetailView.as_view(), name="view_profile"),
    path("profile/edit/", ProfileUpdateView.as_view(), name="edit_profile"),
]
