import pytest
from django.urls import reverse
from django.test import Client
from config.factories import UserFactory, AccountFactory, PlantedTreeFactory


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def user1(db):
    user = UserFactory(username="user1")
    user.set_password("password123")
    user.save()
    return user


@pytest.fixture
def user2(db):
    user = UserFactory(username="user2")
    user.set_password("password123")
    user.save()
    return user


@pytest.fixture
def user3(db):
    user = UserFactory(username="user3")
    user.set_password("password123")
    user.save()
    return user


@pytest.fixture
def account1(user1, user3):
    account = AccountFactory(name="Account 1", created_by=user1)
    account.users.add(user1, user3)
    return account


@pytest.fixture
def account2(user2, user3):
    account = AccountFactory(name="Account 2", created_by=user2)
    account.users.add(user2, user3)
    return account


@pytest.fixture
def planted_tree1(user1, account1):
    return PlantedTreeFactory(user=user1, account=account1)


@pytest.fixture
def planted_tree2(user2, account2):
    return PlantedTreeFactory(user=user2, account=account2)


@pytest.fixture
def planted_tree3(user3, account1):
    return PlantedTreeFactory(user=user3, account=account1)


@pytest.mark.django_db
def test_template_user_trees_listing(client, user1, planted_tree1):
    assert client.login(username=user1.username, password="password123")
    response = client.get(reverse("trees:tree_list"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_template_other_user_trees_forbidden(client, user1, planted_tree2):
    assert client.login(username=user1.username, password="password123")
    response = client.get(
        reverse("trees:plantedtree-detail", kwargs={"pk": planted_tree2.id})
    )
    assert response.status_code == 403


@pytest.mark.django_db
def test_template_account_member_trees_listing(
    client, user3, planted_tree1, planted_tree2, planted_tree3
):
    assert client.login(username=user3.username, password="password123")
    response = client.get(reverse("trees:tree_list"))
    assert response.status_code == 200
