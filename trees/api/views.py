from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from django.core.exceptions import ObjectDoesNotExist
from trees.models import PlantedTree, Tree
from accounts.models import Account
from trees.api.serializers import PlantedTreeListSerializer, PlantedTreeDetailSerializer
from rest_framework.decorators import action
from rest_framework.response import Response


class PlantedTreeViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        filter_type = self.request.query_params.get("filter", "all")

        if filter_type == "mine":
            return PlantedTree.objects.filter(user=user).select_related("tree")
        else:
            accounts = user.accounts.all()
            return PlantedTree.objects.filter(account__in=accounts).select_related(
                "tree"
            )

    def get_serializer_class(self):
        if self.action == "list" or self.action == "plant_multiple":
            return PlantedTreeListSerializer
        return PlantedTreeDetailSerializer

    def perform_create(self, serializer):
        user = self.request.user
        tree = serializer.validated_data.get("tree")
        latitude = serializer.validated_data.get("latitude")
        longitude = serializer.validated_data.get("longitude")
        account = serializer.validated_data.get("account")
        age = serializer.validated_data.get("age", 0)
        user.plant_tree(tree, (latitude, longitude), account, age)

    def perform_update(self, serializer):
        instance = self.get_object()
        if instance.user != self.request.user:
            raise PermissionDenied("You do not have permission to update this tree.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise PermissionDenied("You do not have permission to delete this tree.")
        instance.delete()

    @action(detail=False, methods=["post"])
    def plant_multiple(self, request):
        user = self.request.user
        plants = request.data.get("plants", [])

        plant_data = []
        errors = []

        for plant in plants:
            try:
                tree = Tree.objects.get(id=plant["tree_id"])
                latitude = plant["latitude"]
                longitude = plant["longitude"]
                account = Account.objects.get(id=plant["account"])
                age = plant.get("age", 0)
                plant_data.append(
                    {
                        "tree": tree,
                        "location": (latitude, longitude),
                        "account": account,
                        "age": age,
                    }
                )
            except Tree.DoesNotExist:
                errors.append(f"Tree with id {plant['tree_id']} does not exist.")
            except Account.DoesNotExist:
                errors.append(f"Account with id {plant['account']} does not exist.")
            except KeyError as e:
                errors.append(f"Missing required field: {str(e)}")

        if errors:
            return Response({"errors": errors}, status=400)

        user.plant_trees(plant_data)
        return Response({"status": "success"}, status=201)
