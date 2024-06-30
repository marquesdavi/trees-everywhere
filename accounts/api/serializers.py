from rest_framework import serializers
from ..models import Account


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ["id", "name", "active", "created"]

    def validate_name(self, value):
        if len(value) < 3:
            raise serializers.ValidationError(
                "The account name must be at least 3 characters long."
            )
        return value
