import pytest
from django.conf import settings
from rest_framework.test import APIClient


@pytest.fixture(scope="session")
def django_db_setup():
    settings.DATABASES["default"] = {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
        "ATOMIC_REQUESTS": True,
    }


@pytest.fixture
def api_client():
    return APIClient()
