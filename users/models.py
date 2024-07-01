# models.py (app users)

from django.contrib.auth.models import User
from django.db import models
from trees.models import PlantedTree


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    about = models.TextField(blank=True, null=True)
    joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


def plant_tree(self, tree, location, account, age=0):
    latitude, longitude = location
    PlantedTree.objects.create(
        user=self,
        tree=tree,
        latitude=latitude,
        longitude=longitude,
        account=account,
        age=age,
    )


def plant_trees(self, plants):
    planted_trees = []
    for plant in plants:
        tree = plant["tree"]
        latitude, longitude = plant["location"]
        account = plant["account"]
        age = plant.get("age", 0)
        planted_trees.append(
            PlantedTree(
                user=self,
                tree=tree,
                latitude=latitude,
                longitude=longitude,
                account=account,
                age=age,
            )
        )
    PlantedTree.objects.bulk_create(planted_trees)


User.add_to_class("plant_tree", plant_tree)
User.add_to_class("plant_trees", plant_trees)


def create_profile(sender, **kwargs):
    if kwargs["created"]:
        Profile.objects.create(user=kwargs["instance"])


models.signals.post_save.connect(create_profile, sender=User)
