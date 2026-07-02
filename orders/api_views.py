from rest_framework import viewsets, filters, permissions
from .models import Order
from .serializers import OrderSerializer

class OrderViewSet(viewsets.ModelViewSet):
    #ModelViewSet - full CRUD(not like read-only in ProductViewSet)
    serializer_class = OrderSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at','status'] # ?ordering=-created_at
    filterset_fields = ['status'] # ?status=pending

    def get_queryset(self):
        #user see only self orders
        return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        #when oder created -> we auto add user
        serializer.save(user=self.request.user)
