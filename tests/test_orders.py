import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from products.models import Category, Product
from orders.models import Order, OrderItem

@pytest.fixture
def category(db):
    return Category.objects.create(name='Motherboards', slug='motherboards')


@pytest.fixture
def product(db, category):
    return Product.objects.create(
        name='ASUS ROG STRIX B550-F',
        slug='asus-rog-strix-b550-f',
        price=210.99,
        stock=5,
        is_active=True,
        category=category,
        description='ATX motherboard for AMD Ryzen'
    )


@pytest.fixture
def user(db):
    return User.objects.create_user(
        username='testuser',
        password='testpass123',
        email='test@example.com'
    )


@pytest.fixture
def auth_client(client, user):
    # logged-in client
    client.login(username='testuser', password='testpass123')
    return client


@pytest.mark.django_db
def test_checkout_requires_login(client, product):
    # add to cart first
    client.post(reverse('orders:cart_add'), {'product_id': product.id, 'quantity': 1})

    url = reverse('orders:order_create')
    response = client.get(url)

    # anonymous user gets redirected to login
    assert response.status_code == 302
    assert '/login' in response['Location']


@pytest.mark.django_db
def test_checkout_page_loads(auth_client, product):
    # add to cart
    auth_client.post(reverse('orders:cart_add'), {'product_id': product.id, 'quantity': 1})

    url = reverse('orders:order_create')
    response = auth_client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_order_created_on_checkout(auth_client, user, product):
    # add to cart
    auth_client.post(reverse('orders:cart_add'), {'product_id': product.id, 'quantity': 2})

    # submit checkout form
    url = reverse('orders:order_create')
    auth_client.post(url, {
        'first_name': 'Dan',
        'last_name': 'Malaev',
        'email': 'malaev@example.com',
        'phone': '+380991234567',
        'shipping_address': 'Kyiv, Khreshchatyk 1',
        'payment_method': 'card',
    })

    # order exists in DB and belongs to the user
    assert Order.objects.filter(user=user).exists()


@pytest.mark.django_db
def test_order_items_created(auth_client, user, product):
    auth_client.post(reverse('orders:cart_add'), {'product_id': product.id, 'quantity': 2})

    auth_client.post(reverse('orders:order_create'), {
        'first_name': 'John',
        'last_name': 'Doe',
        'email': 'john@example.com',
        'phone': '+380991234567',
        'shipping_address': 'Kyiv, Khreshchatyk 1',
        'payment_method': 'card',
    })

    order = Order.objects.get(user=user)
    item = OrderItem.objects.get(order=order, product=product)
    assert item.quantity == 2


@pytest.mark.django_db
def test_cart_cleared_after_checkout(auth_client, product):
    auth_client.post(reverse('orders:cart_add'), {'product_id': product.id, 'quantity': 1})

    auth_client.post(reverse('orders:order_create'), {
        'first_name': 'John',
        'last_name': 'Doe',
        'email': 'john@example.com',
        'phone': '+380991234567',
        'shipping_address': 'Kyiv, Khreshchatyk 1',
        'payment_method': 'card',
    })

    # session cart must be empty after order is placed
    cart = auth_client.session.get('cart', {})
    assert cart == {}


@pytest.mark.django_db
def test_order_default_status_is_pending(auth_client, user, product):
    auth_client.post(reverse('orders:cart_add'), {'product_id': product.id, 'quantity': 1})

    auth_client.post(reverse('orders:order_create'), {
        'first_name': 'John',
        'last_name': 'Doe',
        'email': 'john@example.com',
        'phone': '+380991234567',
        'shipping_address': 'Kyiv, Khreshchatyk 1',
        'payment_method': 'card',
    })

    auth_client.post(reverse('orders:order_create'), {
        'first_name': 'John',
        'last_name': 'Doe',
        'email': 'john@example.com',
        'phone': '+380991234567',
        'shipping_address': 'Kyiv, Khreshchatyk 1',
        'payment_method': 'card',
    })

    order = Order.objects.get(user=user)
    assert order.status == 'pending'

#redirect anonymous users to the login page
#load the checkout page
#create an order in the database
#create an OrderItem with the correct quantity
#clear the shopping cart after checkout
#set the default order status to “pending”
