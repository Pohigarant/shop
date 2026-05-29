import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from categories.models import Category


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user(db):
    User = get_user_model()
    return User.objects.create_user(username='testuser', password='testpass')

@pytest.fixture
def admin_user(db):
    User = get_user_model()
    return User.objects.create_user(
        username='admin',
        password='adminpass',
        is_staff=True,      # даём права администратора
        # is_superuser=True  # можно и так, но staff обычно достаточно
    )

@pytest.fixture
def auth_client(api_client, user):
    api_client.force_authenticate(user=user)
    return api_client


@pytest.fixture
def admin_client(api_client, admin_user):
    api_client.force_authenticate(user=admin_user)
    return api_client

