from django.test import TestCase
from accounts.models import Account
from config.factories import UserFactory, AccountFactory


class AccountModelTests(TestCase):
    def test_account_creation(self):
        user = UserFactory()
        account = AccountFactory(created_by=user)
        self.assertEqual(account.created_by, user)
        self.assertTrue(Account.objects.filter(id=account.id).exists())

    def test_account_str_method(self):
        account = AccountFactory(name="Test Account")
        self.assertEqual(str(account), "Test Account")
