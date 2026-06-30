from products.models import Product

#constant, key name, under wich the shoping cart is stored the session
CART_SESSION_KEY = 'cart'

class Cart:

    def __init__(self, request) -> None:

        self.session = request.session
        #take a cart from session, if not - create empty cart
        cart = self.session.get(CART_SESSION_KEY)
        if not cart:
            cart = self.session[CART_SESSION_KEY] = {}
        self.cart = cart

    def add(self, product, quantity=1):

        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = 0
        #checking balances
        qty = self.cart[product_id] + quantity
        if qty > product.stock:
            qty = product.stock
        self.cart[product_id] = qty
        self.save()

    def remove(self, product):

        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def update(self, product, quantity):

        product_id = str(product.id)
        if quantity > product.stock:
            quantity = product.stock
        self.cart[product_id] = quantity
        self.save()

    def get_total_price(self):

        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        total = sum(p.price * self.cart[str(p.id)] for p in products)
        return total

    def save(self):
        #we marked session, so django can save session
        self.session.modified = True

    def __iter__(self):
        #with this we can iterate between templates
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            yield {
                'product': product,
                'quantity': self.cart[str(product.id)],
                'total_price': product.price * self.cart[str(product.id)]
            }

    def __len__(self):
        #sum of products in cart
        return sum(self.cart.values())
