import os

import pytest
from django.contrib.auth import get_user_model
from django.core.cache import caches
from rest_framework.test import APIClient


@pytest.fixture(autouse=True)
def _locmem_cache(settings):
    """По умолчанию тесты работают на локальном кэше — redis им не нужен."""
    settings.CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
            "LOCATION": "tests",
        }
    }
    # LocMemCache хранит данные в глобальном словаре по LOCATION, поэтому
    # без явной очистки кэш переживает тест и портит следующие.
    caches["default"].clear()
    yield
    caches["default"].clear()


@pytest.fixture
def redis_cache(settings):
    import redis as redis_lib

    candidates = _redis_test_urls()
    url = None
    errors = []
    for candidate in candidates:
        try:
            client = redis_lib.Redis.from_url(
                candidate, socket_connect_timeout=1
            )
            client.ping()
        except (redis_lib.exceptions.RedisError, OSError) as exc:
            errors.append(f"{candidate}: {exc}")
        else:
            url = candidate
            break
    if url is None:
        pytest.skip("redis не отвечает — " + "; ".join(errors))
    settings.CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.redis.RedisCache",
            "LOCATION": url,
            "KEY_PREFIX": "shop1_test",
            "TIMEOUT": 300,
        }
    }
    cache = caches["default"]
    cache.clear()
    yield cache
    cache.clear()


def _redis_test_urls():
    explicit = os.getenv("REDIS_TEST_URL")
    if explicit:
        return [explicit]
    urls = []
    from_env = os.getenv("REDIS_URL")
    if from_env:
        urls.append(f"{from_env.rstrip('/')}/2")
    urls.append("redis://127.0.0.1:6379/2")
    return urls


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user(db):
    User = get_user_model()
    return User.objects.create_user(username="testuser", password="testpass")


@pytest.fixture
def admin_user(db):
    User = get_user_model()
    return User.objects.create_superuser(
        username="admin", password="adminpass"
    )


@pytest.fixture
def auth_client(api_client, user):
    client = APIClient()
    client.force_authenticate(user=user)
    return client


@pytest.fixture
def admin_client(api_client, admin_user):
    client = APIClient()
    client.force_authenticate(user=admin_user)
    return client
