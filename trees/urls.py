from django.urls import path
from .views import TreeListView, PlantedTreeDetailView, PlantedTreeCreateView

urlpatterns = [
    path("", TreeListView.as_view(), name="tree_list"),
    path(
        "planted/<int:pk>/", PlantedTreeDetailView.as_view(), name="planted_tree_detail"
    ),
    path("plant/", PlantedTreeCreateView.as_view(), name="planted_tree_create"),
]
