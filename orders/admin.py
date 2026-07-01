from django.contrib import admin
from orders.models import Order, OrderItem

#show OrderItem right inside page Order
class OrderItemInline(admin.TabularInline):
    
    model = OrderItem
    #do not show empty strings for adding
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'status', 'total_price', 'created_at']
    #status filter
    list_filter = ['status']
    #user search
    search_fields = ['user__username', 'user__email']
    #showing orders in page 'orders'
    inlines = [OrderItemInline]
    actions = ['mark_as_paid', 'mark_as_shipped']

    def mark_as_paid(self, request, queryset):
        queryset.update(status='paid')
        self.message_user(request, 'Orders up to date.')
    mark_as_paid.short_description = 'Mark as paid'

    def mark_as_shipped(self, request, queryset):
        queryset.update(status='shipped')
        self.message_user(request, 'Orders up to date.')
    mark_as_shipped.short_description = 'Mark as shipped'
