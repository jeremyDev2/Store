import pytest
from django.urls import reverse
from products.models import Category, Product

@pytest.fixture
def category(db):
    return Category.objects.create(name='Processors', slug='processors')

@pytest.fixture
def product(db, category):
    return Product.objects.create(name='AMD Ryzen 5 5600X',
                                  slug='amd-ryzen-5-5600x',
                                  price=299.99,
                                  stock=5,
                                  is_active=True,
                                  category=category,
                                  description='6-core processor for gaming PCs')

@pytest.mark.django_db()
def test_product_list(client, product):
    url = reverse('products:product_list')
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_product_list_search(client, product):
    url = reverse('products:product_list')
    response = client.get(url, {'q': 'Ryzen'})
    assert response.status_code == 200
    assert 'AMD Ryzen 5 5600X' in response.content.decode()

@pytest.mark.django_db
def test_product_filter_by_category(client, product, category):
    url = reverse('products:product_list')
    response = client.get(url, {'category': category.slug})
    assert response.status_code == 200
    assert 'AMD Ryzen 5 5600X' in response.content.decode()

@pytest.mark.django_db
def test_product_detail(client, product):
    url = reverse('products:product_detail', kwargs={'slug': product.slug})
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_inactive_product_hidden(client, category):
    Product.objects.create(
        name='GTX 1050 (discontinued)',
        slug='gtx-1050',
        price=999,
        stock=0,
        is_active=False,
        category=category
    )
    url = reverse('products:product_list')
    response = client.get(url)
    assert 'GTX 1050' not in response.content.decode()
