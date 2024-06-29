from django.urls import path
from .views import AccountListView, AccountCreateView, AccountUpdateView

urlpatterns = [
    path("", AccountListView.as_view(), name="account_list"),
    path("create/", AccountCreateView.as_view(), name="account_create"),
    path("update/<int:pk>/", AccountUpdateView.as_view(), name="account_update"),
]
