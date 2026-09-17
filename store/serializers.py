
from decimal import Decimal

from rest_framework import serializers

from .models import Product, Collection, Review


class CollectionSerializer(serializers.ModelSerializer):
    product_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Collection
        fields = [
            'id',
            'title',
            'product_count',
        ]


class ProductSerializer(serializers.ModelSerializer):
    price_with_tax = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id',
            'title',
            'price',
            'inventory',
            'price_with_tax',
            'collection',
        ]

    def get_price_with_tax(self, product):
        return product.price * Decimal('1.06')


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = [
            'id',
            'customer',
            'description',
            'created_at',
        ]
        
        def save(self, **kwargs):
            product_id = self.context['product_id']
            return Review.objects.create(product_id=product_id, **self.validated_data)

