from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from trees.models import PlantedTree
from trees.api.serializers import PlantedTreeListSerializer, PlantedTreeDetailSerializer


class PlantedTreeViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        accounts = user.accounts.all()
        return PlantedTree.objects.filter(account__in=accounts).select_related("tree")

    def get_serializer_class(self):
        if self.action == "list":
            return PlantedTreeListSerializer
        return PlantedTreeDetailSerializer

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)

    def perform_update(self, serializer):
        instance = self.get_object()
        if instance.user != self.request.user:
            raise PermissionDenied("You do not have permission to update this tree.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise PermissionDenied("You do not have permission to delete this tree.")
        instance.delete()
