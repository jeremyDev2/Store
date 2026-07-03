import pytest
from django.urls import reverse
from products.models import Category, Product

@pytest.fixture
def category(db):
    return Category.objects.create(name='GPU', slug='gpu')


@pytest.fixture
def product(db, category):
    return Product.objects.create(
        name='RTX 4070',
        slug='rtx-4070',
        price=600.99,
        stock=3,
        is_active=True,
        category=category,
        description='Gaming card'
    )


@pytest.mark.django_db
def test_cart_add(client, product):
    # added product to cart
    url = reverse('orders:cart_add')
    response = client.post(url, {'product_id': product.id, 'quantity': 1})
    assert response.status_code == 302  # redirect after we added
    # check to see if the item has appeared in the session
    cart = client.session.get('cart', {})
    assert str(product.id) in cart


@pytest.mark.django_db
def test_cart_add_quantity(client, product):
    # the quantity is stored correctly
    url = reverse('orders:cart_add')
    client.post(url, {'product_id': product.id, 'quantity': 2})
    cart = client.session.get('cart', {})
    assert cart[str(product.id)]['quantity'] == 2


@pytest.mark.django_db
def test_cart_remove(client, product):
    # first - create
    client.post(reverse('orders:cart_add'), {'product_id': product.id, 'quantity': 1})
    # after - delete
    url = reverse('orders:cart_remove', kwargs={'product_id': product.id})
    client.post(url)

    cart = client.session.get('cart', {})
    assert str(product.id) not in cart


@pytest.mark.django_db
def test_cart_update(client, product):
    # add 1, updating to 3
    client.post(reverse('orders:cart_add'), {'product_id': product.id, 'quantity': 1})

    url = reverse('orders:cart_update', kwargs={'product_id': product.id})
    client.post(url, {'quantity': 3})

    cart = client.session.get('cart', {})
    assert cart[str(product.id)]['quantity'] == 3


@pytest.mark.django_db
def test_cart_detail_page(client, product):
    # cart page are open
    client.post(reverse('orders:cart_add'), {'product_id': product.id, 'quantity': 1})

    url = reverse('orders:cart_detail')
    response = client.get(url)
    assert response.status_code == 200
    assert 'RTX 4070' in response.content.decode()

#Adding an item to the cart
#Correctly saving the quantity
#Removing an item from the cart
#Updating the quantity
#The cart page displays the item
