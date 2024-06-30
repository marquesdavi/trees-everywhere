import pytest
from accounts.models import Account
from config.factories import UserFactory, AccountFactory


@pytest.mark.django_db
def test_account_creation():
    user = UserFactory()
    account = AccountFactory(created_by=user)
    assert account.created_by == user
    assert Account.objects.filter(id=account.id).exists()


@pytest.mark.django_db
def test_account_str_method():
    account = AccountFactory(name="Test Account")
    assert str(account) == "Test Account"
