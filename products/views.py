from django.views.generic import DetailView, ListView
from .models import  Product, Category

class ProductListView(ListView):

    model = Product
    template_name = "products/product_list.html"
    context_object_name = "products"
    paginate_by = 12
    
    #lazy sql-query
    def get_queryset(self):
        
        #load category with 1 join-query and avoided n+1
        queryset = Product.objects.filter(is_active = True).select_related('category')
        
        #Retrieves the value associated with the ‘q’ key. If the parameter is not present in the URL, it returns None.
        query = self.request.GET.get('q')
        if query:
            #__icontains - case-insensetive search (we search in "name" & description fields)
            queryset = queryset.filter(name__icontains=query) | queryset.filter(description__icontains=query)
        
        #Retrieves the value associated with the ‘q’ key.
        category_slug = self.request.GET.get("category")
        if category_slug:
            queryset = queryset.filter(category__slug = category_slug)

        max_price = self.request.GET.get("max_price")
        min_price = self.request.GET.get("min_price")
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        if min_price:
            queryset = queryset.filter(price__gte=min_price)

        #sorting. new - first
        sort = self.request.GET.get('sort', '-created_at')
        allowed_sorts = ["price", "-price", "-created_at", "name"]
        if sort in allowed_sorts:
            queryset = queryset.order_by(sort)
        return queryset

    #interface for filtrating
    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

class ProductDetailView(DetailView):

    model = Product
    template_name = "products/product_detail.html"
    context_object_name = "product"
    # Django automatically looks up an object by its URL slug (<slug:slug>)
