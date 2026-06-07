import pytest

from django.urls import reverse


from categories.models import Category
from products.models import Product



@pytest.fixture
def category(db):
    return Category.objects.create(name='Test Category')

@pytest.fixture
def product(category):
    return Product.objects.create(name='Test Product',category= category, price= 5.00)


def test_list_is_public(api_client,product):
    response = api_client.get(reverse('product-list'))
    assert response.status_code == 200
    assert response.data['count'] == 1
    assert response.data['results'][0]['name'] == 'Test Product'

def test_retrieve_is_public(api_client,product):
    response = api_client.get(reverse('product-detail',kwargs = {'pk':product.pk}))
    assert response.status_code == 200
    assert response.data['name'] == 'Test Product'


@pytest.mark.parametrize('client_fixture,exepted_status',[
    pytest.param('api_client', 403, id='anonymous'),
    pytest.param('auth_client', 403, id='user'),
    pytest.param('admin_client', 201, id='admin'),
     ])
@pytest.mark.django_db
def test_created_permissions(request,client_fixture,exepted_status):
    client = request.getfixturevalue(client_fixture)
    data = {"name": "Test Product", "price": 5.00}
    response = client.post(reverse('product-list'), data, format='json')
    assert response.status_code == exepted_status

def test_popular_is_public(api_client,product):
    response = api_client.get(reverse('product-popular'))
    assert response.status_code == 200

@pytest.mark.django_db
def test_list_uses_list_serializer(api_client, product):

    response = api_client.get(reverse('product-list'))
    item = response.data['results'][0]
    assert item['category'] == "Test Category"      # SlugRelatedField, не вложенный объект
    assert set(item.keys()) == {"id", "name", "price", "category"}


@pytest.mark.parametrize('client_fixture,exepted_status',[
pytest.param('api_client', 403, id='anonymous'),
    pytest.param('auth_client', 403, id='user'),
    pytest.param('admin_client', 204, id='admin'),
])
@pytest.mark.django_db
def test_delete_product(request,client_fixture,product,exepted_status):
    client = request.getfixturevalue(client_fixture)
    url = reverse('product-detail', kwargs={'pk': product.pk})
    response = client.delete(url)
    assert response.status_code == exepted_status


@pytest.mark.parametrize('client_fixture,exepted_status',[
pytest.param('api_client', 403, id='anonymous'),
    pytest.param('auth_client', 403, id='user'),
    pytest.param('admin_client', 200, id='admin'),
])
@pytest.mark.django_db
def test_update_product(request,client_fixture,product,exepted_status):
    client = request.getfixturevalue(client_fixture)
    url = reverse('product-detail', kwargs={'pk': product.pk})
    data = {"name": "New Product", "price": 5.00}
    response = client.patch(url,data, format='json')
    assert response.status_code == exepted_status
