from django.test import TestCase
from rest_framework.test import APIClient
from accounts.models import Account
from config.factories import UserFactory, AccountFactory


class AccountAPITests(TestCase):
    def setUp(self):
        self.user1 = UserFactory(username="user1", password="password123")
        self.user2 = UserFactory(username="user2", password="password123")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user1)

    def test_create_account(self):
        response = self.client.post("/api/accounts/", {"name": "New Account"})
        self.assertEqual(response.status_code, 201)
        self.assertTrue(
            Account.objects.filter(name="New Account", created_by=self.user1).exists()
        )

    def test_update_account(self):
        account = AccountFactory(created_by=self.user1)
        self.client.force_authenticate(user=self.user1)
        response = self.client.put(
            f"/api/accounts/{account.id}/", {"name": "Updated Account", "active": True}
        )
        self.assertEqual(response.status_code, 200)
        account.refresh_from_db()
        self.assertEqual(account.name, "Updated Account")

    def test_update_account_permission_denied(self):
        account = AccountFactory(created_by=self.user1)
        self.client.force_authenticate(user=self.user2)
        response = self.client.put(
            f"/api/accounts/{account.id}/", {"name": "Updated Account", "active": True}
        )
        self.assertEqual(response.status_code, 403)

    def test_delete_account(self):
        account = AccountFactory(created_by=self.user1)
        self.client.force_authenticate(user=self.user1)
        response = self.client.delete(f"/api/accounts/{account.id}/")
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Account.objects.filter(id=account.id).exists())

    def test_delete_account_permission_denied(self):
        account = AccountFactory(created_by=self.user1)
        self.client.force_authenticate(user=self.user2)
        response = self.client.delete(f"/api/accounts/{account.id}/")
        self.assertEqual(response.status_code, 403)

    def test_list_accounts(self):
        # Create accounts for two different users
        account1 = AccountFactory(created_by=self.user1)
        account1.users.add(self.user1)
        account2 = AccountFactory(created_by=self.user2)
        account2.users.add(self.user2)

        # Authenticate as user1 and check they see only their own accounts
        self.client.force_authenticate(user=self.user1)
        response = self.client.get("/api/accounts/")
        self.assertEqual(response.status_code, 200)
        accounts = response.json()
        self.assertEqual(len(accounts["results"]), 1)
        self.assertEqual(accounts["results"][0]["id"], account1.id)

        # Authenticate as user2 and check they see only their own accounts
        self.client.force_authenticate(user=self.user2)
        response = self.client.get("/api/accounts/")
        self.assertEqual(response.status_code, 200)
        accounts = response.json()
        self.assertEqual(len(accounts["results"]), 1)
        self.assertEqual(accounts["results"][0]["id"], account2.id)

        # Authenticate again as user1 to ensure they do not see user2's accounts
        self.client.force_authenticate(user=self.user1)
        response = self.client.get("/api/accounts/")
        self.assertEqual(response.status_code, 200)
        accounts = response.json()
        self.assertEqual(len(accounts["results"]), 1)
        self.assertEqual(accounts["results"][0]["id"], account1.id)
