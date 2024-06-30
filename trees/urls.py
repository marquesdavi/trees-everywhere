from django.urls import path
from .views import TreeListView

urlpatterns = [
    path("", TreeListView.as_view(), name="tree_list"),
]
