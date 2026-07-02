from rest_framework import serializers
from .models import Category, Product

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        #fields to JSON
        fields = ['id', 'name', 'slug']


class ProductSerializer(serializers.ModelSerializer):
    #category name
    category = CategorySerializer(read_only=True)

    class Meta:

        model = Product
        fields = ['id', 'name', 'slug', 'description', 'price', 'stock', 'image', 'category']

