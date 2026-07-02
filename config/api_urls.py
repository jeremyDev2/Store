from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from products.api_views import ProductViewSet, CategoryViewSet
from orders.api_views import OrderViewSet
from reviews.api_views import ReviewViewSet
from users.api_views import RegisterView, ProfileView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

router = DefaultRouter()
router.register('products', ProductViewSet, basename='product')
router.register('categories', CategoryViewSet, basename='category')
router.register('orders', OrderViewSet, basename='order')
router.register(r'products/(?P<product_pk>\d+)/reviews', ReviewViewSet, basename='review')

urlpatterns = [
    path('', include(router.urls)),
    #JWT tokens
    path('token/', TokenObtainPairView.as_view(), name='token_obtain'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    #users
    path('users/register/', RegisterView.as_view(), name='register'),
    path('users/profile/', ProfileView.as_view(), name='profile'),
    #swagger
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
