from django.urls import path
from .views import AccountTemplateView

urlpatterns = [
    path("", AccountTemplateView.as_view(), name="account_list"),
]
