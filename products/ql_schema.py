import graphene
from graphene_django import DjangoObjectType
from .models import Product, Category

class CategoryType(DjangoObjectType):

    class Meta:
        model=Category
        fields = ('id', 'name', 'slug')

class ProductType(DjangoObjectType):

    class Meta:
        model = Product
        fields = ('id', 'name', 'slug', 'description', 'price', 'stock', 'is_active', 'category')

class Query(graphene.ObjectType):

    all_products = graphene.List(ProductType,
                                 search=graphene.String(),
                                 category_slug=graphene.String(),
                                 min_price=graphene.Float(),
                                 max_price=graphene.Float(),)
    
    product = graphene.Field(ProductType, slug=graphene.String(required=True))
    all_categories = graphene.List(CategoryType)

    def resolve_all_products(root, info, search=None, category_slug=None, min_price=None, max_price=None):
        #list of products(the category is fetched using `select_related` to avoid the N+1 problem, but the `queryset` contains the products.)
        queryset = Product.objects.filter(is_active=True).select_related('category')
        
        #search - parameter that the user passes in the request. (query { allProducts(search: "Ryzen") { name } })
        if search:
            #filter - return list even have one result ([<Product: RTX 4070>])
            queryset = queryset.filter(name__icontains=search)
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        if min_price is not None: 
            queryset = queryset.filter(price__gte=min_price)
        if max_price is not None:
            queryset = queryset.filter(price__lte=max_price)
        return queryset

    def resolve_product(root, info, slug):
        #get - return object (<Product: RTX 4070>)
        return Product.objects.select_related('category').get(slug=slug)

    def resolve_all_categories(root, info):
        return Category.objects.all()
