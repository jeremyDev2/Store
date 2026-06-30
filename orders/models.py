from django.db import models
from products.models import Product
from django.contrib.auth.models import User

STATUS = [
    ('pending', 'Pending'),
    ('paid', 'Paid'),
    ('shipped', 'Shipped'),
    ('delivered', 'Delivered'),
    ('cancelled', 'Cancelled'),
]

class Order(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    status = models.CharField(max_length=20, choices=STATUS, default='pending')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class OrderItem(models.Model):

    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
