from django.test import TestCase
from django.urls import reverse
from config.factories import (
    UserFactory,
    AccountFactory,
    TreeFactory,
    PlantedTreeFactory,
)
from trees.models import PlantedTree
from decimal import Decimal
from django.core.exceptions import ValidationError


class PlantedTreeTemplateTests(TestCase):
    def setUp(self):
        self.user1 = UserFactory.create(username="user1")
        self.user2 = UserFactory.create(username="user2")
        self.account1 = AccountFactory.create(name="Account1", users=[self.user1])
        self.account2 = AccountFactory.create(name="Account2", users=[self.user2])
        self.tree1 = TreeFactory.create(name="Tree1", scientific_name="ScientificTree1")
        self.tree2 = TreeFactory.create(name="Tree2", scientific_name="ScientificTree2")
        self.planted_tree1 = PlantedTreeFactory.create(
            age=5,
            user=self.user1,
            tree=self.tree1,
            account=self.account1,
            latitude=Decimal("10.000000"),
            longitude=Decimal("20.000000"),
        )
        self.planted_tree2 = PlantedTreeFactory.create(
            age=10,
            user=self.user2,
            tree=self.tree2,
            account=self.account2,
            latitude=Decimal("15.000000"),
            longitude=Decimal("25.000000"),
        )

    def test_user_can_view_own_trees(self):
        self.client.login(username="user1", password="password123")
        response = self.client.get(reverse("planted_tree_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.planted_tree1.tree.name)
        self.assertNotContains(response, self.planted_tree2.tree.name)

    def test_user_cannot_view_others_trees(self):
        self.client.login(username="user1", password="password123")
        response = self.client.get(
            reverse("planted_tree_detail", args=[self.planted_tree2.id])
        )
        self.assertEqual(response.status_code, 403)

    def test_user_can_view_account_trees(self):
        self.client.login(username="user1", password="password123")
        response = self.client.get(reverse("planted_tree_list"), {"filter": "all"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.planted_tree1.tree.name)


class UserPlantTreeTests(TestCase):
    def setUp(self):
        self.user = UserFactory.create(username="user", password="password123")
        self.account = AccountFactory.create(name="Account1", users=[self.user])
        self.tree = TreeFactory.create(name="Tree", scientific_name="ScientificTree")

    def test_plant_tree(self):
        self.user.plant_tree(
            self.tree, (Decimal("10.000000"), Decimal("20.000000")), self.account, 5
        )
        self.assertEqual(PlantedTree.objects.count(), 1)
        planted_tree = PlantedTree.objects.first()
        self.assertEqual(planted_tree.user, self.user)
        self.assertEqual(planted_tree.tree, self.tree)
        self.assertEqual(planted_tree.account, self.account)
        self.assertEqual(planted_tree.latitude, Decimal("10.000000"))
        self.assertEqual(planted_tree.longitude, Decimal("20.000000"))
        self.assertEqual(planted_tree.age, 5)

    def test_plant_tree_invalid_coordinates(self):
        with self.assertRaises(ValidationError):
            self.user.plant_tree(
                self.tree,
                (Decimal("100.000000"), Decimal("200.000000")),
                self.account,
                5,
            )

    def test_plant_tree_not_in_account(self):
        other_account = AccountFactory.create(name="Account2")
        with self.assertRaises(ValidationError):
            self.user.plant_tree(
                self.tree,
                (Decimal("10.000000"), Decimal("20.000000")),
                other_account,
                5,
            )

    def test_plant_trees(self):
        plants = [
            {
                "tree": self.tree,
                "location": (Decimal("10.000000"), Decimal("20.000000")),
                "account": self.account,
                "age": 5,
            },
            {
                "tree": self.tree,
                "location": (Decimal("15.000000"), Decimal("25.000000")),
                "account": self.account,
                "age": 10,
            },
        ]
        self.user.plant_trees(plants)
        self.assertEqual(PlantedTree.objects.count(), 2)
