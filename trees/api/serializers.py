from rest_framework import serializers
from trees.models import PlantedTree, Tree


class TreeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tree
        fields = ["name", "scientific_name"]


class PlantedTreeListSerializer(serializers.ModelSerializer):
    tree = TreeSerializer(read_only=True)

    class Meta:
        model = PlantedTree
        fields = ["id", "tree", "age"]
