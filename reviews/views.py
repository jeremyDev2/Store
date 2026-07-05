from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views import View
from products.models import Product
from orders.models import OrderItem
from .models import Review

class AddReviewView(View):

    def get(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        return render(request, 'reviews/add_review.html', {'product': product})

    def post(self, request, product_id):
        
        product = get_object_or_404(Product, id=product_id)
        #check if user buy something. exist() - check DB and if we have the record - True
        has_purchased = OrderItem.objects.filter(order__user=request.user, product=product).exists()

        if not has_purchased:
            messages.error(request, "You can write the review only after you buy product.")
            return redirect('products:product_detail', slug=product.slug)
        
        #from POST-data dict, get value from key "rating" or "comment"
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        
        Review.objects.create(product=product, user=request.user, rating=rating, comment=comment)

        return redirect("products:product_detail", slug=product.slug)
