import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from categories.models import Category
from tests.conftest import auth_client


@pytest.mark.django_db
def test_categories_list_status(api_client):
    url = reverse('category-list')
    response = api_client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_create_category_anonymous_fails(api_client):
    url = reverse('category-list')
    data = {"name": "Электроника"}
    response = api_client.post(url, data, format='json')
    assert response.status_code == 403   # аноним не имеет прав

@pytest.mark.django_db
def test_create_category_user_fails(auth_client):
    url = reverse('category-list')
    data = {"name": "Электроника"}
    response = auth_client.post(url, data, format='json')
    assert response.status_code == 403   # обычный пользователь не админ

@pytest.mark.django_db
def test_create_category_admin_succeeds(admin_client):
    url = reverse('category-list')
    data = {"name": "Электроника"}
    response = admin_client.post(url, data, format='json')
    assert response.status_code == 201
    assert response.data['name'] == "Электроника"
    assert Category.objects.count() == 1
    assert Category.objects.first().name == "Электроника"

@pytest.mark.django_db
def test_update_category_anonymous_fails(api_client,existing_category):
    url = reverse('category-detail', kwargs = {'pk': existing_category.id })
    data = {'name': 'Новое название'}
    response = api_client.put(url, data, format='json')
    assert response.status_code == 403

@pytest.mark.django_db
def test_delete_category_anonymous_fails(api_client, existing_category):
    url = reverse('category-detail', kwargs={'pk': existing_category.id})
    response = api_client.delete(url)
    assert response.status_code == 403

@pytest.mark.django_db
def test_update_category_user_fails(auth_client, existing_category):
    url = reverse('category-detail', kwargs={'pk': existing_category.id})
    data = {"name": "Новое название"}
    response = auth_client.put(url, data, format='json')
    assert response.status_code == 403

@pytest.mark.django_db
def test_delete_category_user_fails(api_client, existing_category):
    url = reverse('category-detail', kwargs={'pk': existing_category.id})
    response = api_client.delete(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_update_category_admin_succeeds(admin_client, existing_category):
    url = reverse('category-detail', kwargs={'pk': existing_category.id})
    data = {"name": "Обновлённое имя"}
    response = admin_client.put(url, data, format='json')
    assert response.status_code == 200
    assert response.data['name'] == "Обновлённое имя"

    existing_category.refresh_from_db()
    assert existing_category.name == "Обновлённое имя"


@pytest.mark.django_db
def test_partial_update_category_admin_succeeds(admin_client, existing_category):
    url = reverse('category-detail', kwargs={'pk': existing_category.id})
    data = {"name": "Частично обновлено"}
    response = admin_client.patch(url, data, format='json')
    assert response.status_code == 200
    assert response.data['name'] == "Частично обновлено"

    existing_category.refresh_from_db()
    assert existing_category.name == "Частично обновлено"


@pytest.mark.django_db
def test_delete_category_admin_succeeds(admin_client, existing_category):
    url = reverse('category-detail', kwargs={'pk': existing_category.id})
    response = admin_client.delete(url)
    assert response.status_code == 204

    from categories.models import Category
    assert not Category.objects.filter(id=existing_category.id).exists()