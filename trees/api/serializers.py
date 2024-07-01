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

    def validate_latitude(self, value):
        if not -90 <= value <= 90:
            raise serializers.ValidationError(
                "Latitude must be between -90 and 90 degrees."
            )
        return value

    def validate_longitude(self, value):
        if not -180 <= value <= 180:
            raise serializers.ValidationError(
                "Longitude must be between -180 and 180 degrees."
            )
        return value

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


class PlantMultipleTreesSerializer(serializers.Serializer):
    tree_id = serializers.PrimaryKeyRelatedField(queryset=Tree.objects.all())
    latitude = serializers.DecimalField(max_digits=9, decimal_places=6)
    longitude = serializers.DecimalField(max_digits=9, decimal_places=6)
    account = serializers.PrimaryKeyRelatedField(queryset=Account.objects.all())
    age = serializers.IntegerField(required=False, default=0)

    def validate_latitude(self, value):
        if not -90 <= value <= 90:
            raise serializers.ValidationError(
                "Latitude must be between -90 and 90 degrees."
            )
        return value

    def validate_longitude(self, value):
        if not -180 <= value <= 180:
            raise serializers.ValidationError(
                "Longitude must be between -180 and 180 degrees."
            )
        return value

    def validate(self, data):
        if "tree_id" not in data:
            raise serializers.ValidationError("Tree ID is required.")
        if "latitude" not in data:
            raise serializers.ValidationError("Latitude is required.")
        if "longitude" not in data:
            raise serializers.ValidationError("Longitude is required.")
        if "account" not in data:
            raise serializers.ValidationError("Account is required.")
        return data

    def create(self, validated_data):
        user = self.context["request"].user
        plants_data = validated_data.pop("plants")
        user.plant_trees(plants_data)
        return validated_data
