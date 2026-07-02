from rest_framework import serializers
from .models import Review

class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = ["id", "product", "user", "rating", "comment", "created_at"]
        #because "product" we take from URL, and we dont need this here
        read_only_fields = ["id", "user", "created_at"]
