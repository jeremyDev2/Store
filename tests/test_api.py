import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from products.models import Category, Product
from orders.models import Order

@pytest.fixture
def category(db):
    return Category.objects.create(name='RAM',slug='ram')

@pytest.fixture
def product(db, category):
    return Product.objects.create(
        name='Kingston Fury 16GB DDR5',
        slug='kingston-fury-16gb-ddr5',
        price=99.99,
        stock=10,
        is_active=True,
        category=category,
        description='DDR5 gaming RAM'
    )

@pytest.fixture
def user(db):
    return User.objects.create_user(
        username='testuser',
        password='testpass123',
        email='test@example.com'
    )

@pytest.fixture
def jwt_token(client,user):
    #get JWT access token for the user(real POST-query(no-hardcode))
    url = reverse('token_obtain')
    response = client.post(url, {
        'username':'testuser',
        'password':'testpass123',
    }, content_type='application/json')
    return response.data['access']

@pytest.fixture
def auth_headers(jwt_token):
    return {'HTTP_AUTHORIZATION': f'Bearer {jwt_token}'}

@pytest.mark.django_db
def test_api_product_list(client,product):
    # public endpoint, no auth required
    url = reverse('product-list')
    response = client.get(url)
    assert response.status_code == 200
    assert response.data['count'] == 1


@pytest.mark.django_db
def test_api_product_detail(client, product):
    url = reverse('product-detail', kwargs={'pk': product.id})
    response = client.get(url)
    assert response.status_code == 200
    assert response.data['name'] == 'Kingston Fury 16GB DDR5'

@pytest.mark.django_db
def test_api_product_search(client, product):
    url = reverse('product-list')
    response = client.get(url, {'search': 'Kingston'})
    assert response.status_code == 200
    assert response.data['count'] == 1

@pytest.mark.django_db
def test_api_category_list(client, category):
    url = reverse('category-list')
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_jwt_obtain_token(client, user):
    url = reverse('token_obtain')
    response = client.post(url, {
        'username': 'testuser',
        'password': 'testpass123',
    }, content_type='application/json')
    assert response.status_code == 200
    assert 'access' in response.data
    assert 'refresh' in response.data

@pytest.mark.django_db
def test_jwt_wrong_credentials(client,user):
    url = reverse('token_obtain')
    response = client.post(url, {
        'username':'testuser',
        'password':'wrongpassword',
    }, content_type='application/json')
    assert response.status_code == 401


@pytest.mark.django_db
def test_api_orders_requires_auth(client):
    # anonymous user gets 401
    url = reverse('order-list')
    response = client.get(url)
    assert response.status_code == 401

@pytest.mark.django_db
def test_api_orders_authenticated(client, user, auth_headers):
    #transform URL name in path( reverse('order-list')  →  '/api/orders/' )
    url = reverse('order-list')
    response = client.get(url, **auth_headers)
    assert response.status_code == 200


@pytest.mark.django_db
#auth_headers - parametr expanded to HTTP_AUTHORIZATION=Bearer(HTTP-header that a client sends to the server to prove that it is authorized)
def test_api_orders_only_own(client, user,auth_headers, product):
    #create order for this user
    order = Order.objects.create(user=user, total_price=99.99, status='pending')

    #create another user with their own order
    other_user = User.objects.create_user(username='other', password='pass123')
    Order.objects.create(user=other_user, total_price=100, status='pending')

    url = reverse('order-list')
    response = client.get(url, **auth_headers)

    #user sees only their own order, not the other user's
    assert response.data['count'] == 1
    assert response.data['results'][0]['id'] == order.id

@pytest.mark.django_db
def test_api_profile_requires_auth(client):
    url = reverse('profile')
    response = client.get(url)
    assert response.status_code == 401

@pytest.mark.django_db
def test_api_profile_returns_user_data(client,user, auth_headers):
    url = reverse('profile')
    response = client.get(url, **auth_headers)
    assert response.status_code == 200
    assert response.data['username'] == 'testuser'


@pytest.mark.django_db
def test_api_register(client):
    url = reverse('register')
    response = client.post(url, {
        'username':'newuser',
        'email':'new@example.com',
        'password':'securepass123',
    }, content_type='application/json')
    assert response.status_code == 201
    assert User.objects.filter(username='newuser').exists()
