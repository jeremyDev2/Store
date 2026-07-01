from django.contrib import admin
from .models import Category, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    #column in list, search on name, autocomplite slug from name
    list_display = ["name", "slug", "parent"]
    search_fields = ['name']
    prepopulated_fields = {"slug":('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'stock', 'is_active', 'category', 'created_at']
    list_filter = ['is_active', 'category']
    #search
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    #redacting right in list
    list_editable = ['price', 'stock', 'is_active']
    #custom actions
    actions = ['make_active', 'make_inactive']

    def make_active(self, request, queryset):
        #make orders active
        queryset.update(is_active=True)
    make_active.short_description = 'Make active'

    def make_inactive(self, request, queryset):
        #make orders inactive
        queryset.update(is_active=False)
    make_inactive.short_description = 'Make inactive'
