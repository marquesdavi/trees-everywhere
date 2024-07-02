from django.db import models
from django.contrib.auth.models import User
from accounts.models import Account
from django.core.exceptions import ValidationError


class Tree(models.Model):
    name = models.CharField(max_length=100)
    scientific_name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class PlantedTree(models.Model):
    age = models.IntegerField()
    planted_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tree = models.ForeignKey(Tree, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    def __str__(self):
        return f"{self.tree.name} planted by {self.user.username}"

    def clean(self):
        if not (-90 <= self.latitude <= 90):
            raise ValidationError("Latitude must be between -90 and 90 degrees.")
        if not (-180 <= self.longitude <= 180):
            raise ValidationError("Longitude must be between -180 and 180 degrees.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
