from django.urls import path
from . import views

#namespace
app_name = "products"

urlpatterns = [
    path("", views.ProductListView.as_view(), name='product_list'),
    # left "slug" - converter type, right "slug" - parametr name what view need like kwarhs['slug']
    path("<slug:slug>/", views.ProductDetailView.as_view(), name='product_detail'),
]
