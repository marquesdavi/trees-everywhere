from django.urls import path
from .views import (
    PlantedTreeListView,
    PlantedTreeDetailView,
    PlantedTreeCreateView,
    PlantedTreeUpdateView,
    PlantedTreeDeleteView,
)

urlpatterns = [
    path("", PlantedTreeListView.as_view(), name="planted_tree_list"),
    path(
        "planted-tree/<int:pk>/",
        PlantedTreeDetailView.as_view(),
        name="planted_tree_detail",
    ),
    path(
        "planted-tree/new/", PlantedTreeCreateView.as_view(), name="planted_tree_create"
    ),
    path(
        "planted-tree/<int:pk>/edit/",
        PlantedTreeUpdateView.as_view(),
        name="planted_tree_update",
    ),
    path(
        "planted-tree/<int:pk>/delete/",
        PlantedTreeDeleteView.as_view(),
        name="planted_tree_delete",
    ),
]
