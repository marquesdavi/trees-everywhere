import factory
from django.contrib.auth.models import User
from accounts.models import Account
from trees.models import Tree, PlantedTree


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        skip_postgeneration_save = True

    username = factory.Faker("user_name")
    email = factory.Faker("email")
    password = factory.PostGenerationMethodCall("set_password", "password123")


class AccountFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Account

    name = factory.Faker("company")
    active = factory.Faker("boolean")
    created_by = factory.SubFactory(UserFactory)


class TreeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Tree

    name = factory.Faker("word")
    scientific_name = factory.Faker("word")


class PlantedTreeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PlantedTree

    user = factory.SubFactory(UserFactory)
    tree = factory.SubFactory(TreeFactory)
    latitude = factory.Faker("latitude")
    longitude = factory.Faker("longitude")
    account = factory.SubFactory(AccountFactory)
    age = factory.Faker("random_number", digits=2)
