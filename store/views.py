
from django.db.models import Count

from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Product, Collection, OrderItem, Review
from .serializers import (
    ProductSerializer,
    CollectionSerializer,
    ReviewSerializer,
)


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def destroy(self, request, *args, **kwargs):
        product = self.get_object()

        if OrderItem.objects.filter(product=product).exists():
            return Response(
                {
                    'error': (
                        'Product cannot be deleted because '
                        'it is associated with an order item.'
                    )
                },
                status=status.HTTP_409_CONFLICT
            )

        return super().destroy(request, *args, **kwargs)


class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(
        product_count=Count('products')
    )
    serializer_class = CollectionSerializer

    def destroy(self, request, *args, **kwargs):
        collection = self.get_object()

        if collection.products.exists():
            return Response(
                {
                    'error': (
                        'Collection cannot be deleted because '
                        'it is associated with products.'
                    )
                },
                status=status.HTTP_409_CONFLICT
            )

        return super().destroy(request, *args, **kwargs)


class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

