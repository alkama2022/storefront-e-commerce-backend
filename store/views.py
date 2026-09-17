from django.db.models import Count

from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from store.fielters import ProductFilter
from . import models
from . import serializers


class ProductViewSet(ModelViewSet):
    filter_backends = [DjangoFilterBackend,SearchFilter,OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'name']

    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer

    def destroy(self, request, *args, **kwargs):
        product = self.get_object()

        if models.OrderItem.objects.filter(product=product).exists():
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
    queryset = models.Collection.objects.annotate(
        product_count=Count('products')
    )
    serializer_class = serializers.CollectionSerializer

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
    def get_queryset(self):
        return models.Review.objects.filter(product_id=self.kwargs['product_pk'])
    serializer_class = serializers.ReviewSerializer
    
    def get_serializer_context(self):
        return {'product_id': self.kwargs['product_pk']}

