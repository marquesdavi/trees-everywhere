import pytest
from rest_framework.test import APIClient
from accounts.models import Account
from config.factories import UserFactory, AccountFactory


@pytest.fixture
def user1(db):
    return UserFactory(username="user1", password="password123")


@pytest.fixture
def user2(db):
    return UserFactory(username="user2", password="password123")


@pytest.fixture
def client(user1):
    client = APIClient()
    client.force_authenticate(user=user1)
    return client


@pytest.fixture
def account(user1):
    return AccountFactory(created_by=user1)


@pytest.mark.django_db
def test_create_account(api_client):
    user = UserFactory()
    api_client.force_authenticate(user=user)
    response = api_client.post("/api/accounts/", {"name": "New Account"})
    assert response.status_code == 201
    assert Account.objects.filter(name="New Account", created_by=user).exists()


@pytest.mark.django_db
def test_update_account(api_client, account):
    api_client.force_authenticate(user=account.created_by)
    response = api_client.put(
        f"/api/accounts/{account.id}/", {"name": "Updated Account", "active": True}
    )
    assert response.status_code == 200
    account.refresh_from_db()
    assert account.name == "Updated Account"


@pytest.mark.django_db
def test_update_account_permission_denied(api_client, user2, account):
    api_client.force_authenticate(user=user2)
    response = api_client.put(
        f"/api/accounts/{account.id}/", {"name": "Updated Account", "active": True}
    )
    assert response.status_code == 403


@pytest.mark.django_db
def test_delete_account(api_client, account):
    api_client.force_authenticate(user=account.created_by)
    response = api_client.delete(f"/api/accounts/{account.id}/")
    assert response.status_code == 204
    assert not Account.objects.filter(id=account.id).exists()


@pytest.mark.django_db
def test_delete_account_permission_denied(api_client, user2, account):
    api_client.force_authenticate(user=user2)
    response = api_client.delete(f"/api/accounts/{account.id}/")
    assert response.status_code == 403


@pytest.mark.django_db
def test_list_accounts(api_client, user1, user2):
    # Create accounts for two different users
    account1 = AccountFactory(created_by=user1)
    account2 = AccountFactory(created_by=user2)

    # Authenticate as user1 and check they see only their own accounts
    api_client.force_authenticate(user=user1)
    response = api_client.get("/api/accounts/")
    assert response.status_code == 200
    accounts = response.json()
    assert len(accounts["results"]) == 1
    assert accounts["results"][0]["id"] == account1.id

    # Authenticate as user2 and check they see only their own accounts
    api_client.force_authenticate(user=user2)
    response = api_client.get("/api/accounts/")
    assert response.status_code == 200
    accounts = response.json()
    assert len(accounts["results"]) == 1
    assert accounts["results"][0]["id"] == account2.id

    # Authenticate again as user1 to ensure they do not see user2's accounts
    api_client.force_authenticate(user=user1)
    response = api_client.get("/api/accounts/")
    assert response.status_code == 200
    accounts = response.json()
    assert len(accounts["results"]) == 1
    assert accounts["results"][0]["id"] == account1.id
