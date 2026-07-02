from rest_framework import serializers
from .models import Order, OrderItem

class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ["id", "user", "status", "total_price", "shipping_address", "created_at", "updated_at"]
        read_only_fields = ["id", "user", "total_price", "created_at", "updated_at"]


class OrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        fields = ["id", "order", "product", "quantity", "price"]
        #price fixation on buy moment
        read_only_fields = ["id", "price"]
