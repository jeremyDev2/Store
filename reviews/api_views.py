from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Review
from .serializers import ReviewSerializer

class ReviewViewSet(viewsets.ModelViewSet):

    serializer_class = ReviewSerializer
    #read review's and write if authenticated
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        #return reviews only from product fropm URL(/api/products/1/reviews/). product_pk taked from URL
        return Review.objects.filter(product_id=self.kwargs['product_pk'])

    def perform_create(self, serializer):
        serializer.save(user = self.request.user, 
                        #self.kwargs['product_pk'] - issue to extract product id from URL in ViewSet
                        product_id = self.kwargs['product_pk'])
