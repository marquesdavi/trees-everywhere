from rest_framework import serializers
from ..models import PlantedTree, Tree
from accounts.models import Account


class TreeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tree
        fields = ["name", "scientific_name"]


class PlantedTreeListSerializer(serializers.ModelSerializer):
    tree = TreeSerializer(read_only=True)

    class Meta:
        model = PlantedTree
        fields = ["id", "tree", "age"]


class PlantedTreeDetailSerializer(serializers.ModelSerializer):
    tree = TreeSerializer(read_only=True)
    tree_id = serializers.PrimaryKeyRelatedField(
        queryset=Tree.objects.all(), source="tree"
    )
    account = serializers.PrimaryKeyRelatedField(queryset=Account.objects.all())
    latitude = serializers.DecimalField(max_digits=9, decimal_places=6)
    longitude = serializers.DecimalField(max_digits=9, decimal_places=6)

    class Meta:
        model = PlantedTree
        fields = [
            "id",
            "age",
            "planted_at",
            "tree",
            "tree_id",
            "account",
            "latitude",
            "longitude",
        ]

    def create(self, validated_data):
        return PlantedTree.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.age = validated_data.get("age", instance.age)
        instance.tree = validated_data.get("tree", instance.tree)
        instance.account = validated_data.get("account", instance.account)
        instance.latitude = validated_data.get("latitude", instance.latitude)
        instance.longitude = validated_data.get("longitude", instance.longitude)
        instance.save()
        return instance
