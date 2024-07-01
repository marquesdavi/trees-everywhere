from django.contrib.auth.models import User
from trees.models import PlantedTree


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
