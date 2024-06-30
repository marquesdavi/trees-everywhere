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
    for tree, location, account, age in plants:
        self.plant_tree(tree, location, account, age)


User.add_to_class("plant_tree", plant_tree)
User.add_to_class("plant_trees", plant_trees)
