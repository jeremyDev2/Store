from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from products.models import Product
from .cart import CART_SESSION_KEY, Cart
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.conf import settings
from django.db import transaction
from .forms import PlaceOrderForm
from .models import Order, OrderItem

class CartDetailView(View):

    def get(self, request):
        cart = Cart(request)
        return render(request, 'orders/cart.html', {'cart': cart})


class CartAddView(View):

    def post(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        quantity = int(request.POST.get('quantity', 1))
        cart.add(product, quantity)
        return redirect('orders:cart_detail')

class CartRemoveView(View):

    def post(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        cart.remove(product)
        return redirect('orders:cart_detail')

class CartUpdateView(View):

    def post(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        quantity = int(request.POST.get('quantity', 1))
        cart.update(product, quantity)
        return redirect('orders:cart_detail')

#create order using cart
class OrderCreateView(LoginRequiredMixin, View):
    
    #order page with form and cart product's
    def get(self, request):
        cart = Cart(request)
        form = PlaceOrderForm()
        return render(request, "orders/checkout.html", {"cart": cart, 'form':form})

    def post(self, request):
        cart = Cart(request)
        form = PlaceOrderForm(request.POST)

        if not form.is_valid():
            return render(request, "orders/checkout.html", {"cart": cart, 'form':form})

        #atomic transaction
        with transaction.atomic():
            order = Order.objects.create(user=request.user, 
                                         total_price=cart.get_total_price(),
                                         shipping_address = form.cleaned_data['shipping_address'],
                                         )
            for item in cart:
                OrderItem.objects.create(order=order, 
                                         product=item['product'],
                                         quantity=item['quantity'],
                                         #price in moment when we order
                                         price=item['product'].price,
                                         )
                item['product'].stock -= item['quantity']
                item['product'].save()
        
        #clear cart from session after success order
        del request.session[CART_SESSION_KEY]

        send_mail(subject=f"Order #{order.id}",
                  message=f"Thank you! Cost: {order.total_price}",
                  from_email=settings.DEFAULT_FROM_EMAIL,
                  recipient_list=[request.user.email],
                  )
        return redirect('orders:cart_detail')
