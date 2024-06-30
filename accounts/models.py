from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class Account(models.Model):
    name = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    users = models.ManyToManyField(User, related_name="accounts")
    created_by = models.ForeignKey(
        User, related_name="created_accounts", on_delete=models.CASCADE, default=1
    )

    def clean(self):
        if not self.name:
            raise ValidationError("The account name cannot be empty.")
        if len(self.name) < 3:
            raise ValidationError(
                "The account name must be at least 3 characters long."
            )

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
