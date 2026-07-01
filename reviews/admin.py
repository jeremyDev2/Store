from django.contrib import admin
from reviews.models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):

    list_display = ['product', 'user', 'rating', 'created_at']
    #rating filter
    list_filter = ['rating']
    #product & user search
    search_fields = ['product__name', 'user__username']
