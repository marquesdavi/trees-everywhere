import factory
from django.contrib.auth.models import User
from accounts.models import Account


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
