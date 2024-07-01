import pytest
from rest_framework.test import APIClient
from config.factories import UserFactory, AccountFactory, PlantedTreeFactory


@pytest.fixture
def api_client():
    return APIClient()


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
def account1(user1):
    account = AccountFactory(name="Account 1", created_by=user1)
    account.users.add(user1)
    return account


@pytest.fixture
def account2(user2):
    account = AccountFactory(name="Account 2", created_by=user2)
    account.users.add(user2)
    return account


@pytest.fixture
def planted_tree1(user1, account1):
    return PlantedTreeFactory(user=user1, account=account1)


@pytest.fixture
def planted_tree2(user2, account2):
    return PlantedTreeFactory(user=user2, account=account2)


@pytest.mark.django_db
def test_user_trees_listing(api_client, user1, planted_tree1):
    api_client.force_authenticate(user=user1)
    response = api_client.get("/api/trees/planted-trees/")
    assert response.status_code == 200
    results = response.json()["results"]
    assert len(results) == 1
    assert results[0]["id"] == planted_tree1.id


@pytest.mark.django_db
def test_other_user_trees_forbidden(api_client, user1, user2, planted_tree2):
    api_client.force_authenticate(user=user1)
    response = api_client.get(f"/api/trees/planted-trees/{planted_tree2.id}/")
    print("Response Status Code:", response.status_code)
    print("Response Content:", response.content.decode())
    assert response.status_code == 403
