from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("products/", include("products.urls")),
    path('reviews/', include('reviews.urls')),
    path('orders/', include("orders.urls")),
    path('users/', include('users.urls')),
    path('api/', include('config.api_urls')),
]
