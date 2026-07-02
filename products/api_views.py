from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer

class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    # ReadOnlyModelViewSet - only get query's
    queryset = Product.objects.filter(is_active=True).select_related('category')
    serializer_class = ProductSerializer
    # DjangoFilterBackend - ?category=1 (example) return items only from category 
    # SearchFilter - ?search=iphone (example). Search on name and description, using LIKE
    # OrderingFilter - ?ordering=price/-price(example) ordering from ascending to descending 
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category'] # ?category=1
    search_fields = ['name', 'description'] # ?search=iphone
    ordering_fields = ['price', 'created_at'] # ?ordering=price

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
