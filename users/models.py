from django.contrib.auth.models import User
from trees.models import Tree, PlantedTree


def plant_tree(self, tree, location):
    latitude, longitude = location
    PlantedTree.objects.create(
        user=self, tree=tree, latitude=latitude, longitude=longitude
    )


def plant_trees(self, plants):
    for tree, location in plants:
        self.plant_tree(tree, location)


User.add_to_class("plant_tree", plant_tree)
User.add_to_class("plant_trees", plant_trees)
