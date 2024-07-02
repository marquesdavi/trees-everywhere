from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from trees.models import PlantedTree
from trees.api.serializers import PlantedTreeListSerializer
from rest_framework.response import Response
from rest_framework.decorators import action


class PlantedTreeViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = PlantedTreeListSerializer

    def get_queryset(self):
        return PlantedTree.objects.filter(user=self.request.user).select_related("tree")

    @action(detail=False, methods=["get"], url_path="user-trees")
    def user_trees(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
