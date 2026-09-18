from django.contrib.admin import filters
from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.permissions import IsAuthenticated,IsAdminUser,DjangoModelPermissions
from rest_framework import status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet,GenericViewSet
from rest_framework.mixins import CreateModelMixin,RetrieveModelMixin,DestroyModelMixin,UpdateModelMixin
from rest_framework.decorators import action
from store.fielters import ProductFilter
from store.pagination import DefaultPagination
from store.permisions import IsAdminOrReadOnly
from . import models
from . import serializers



class ProductViewSet(ModelViewSet):
    filter_backends = [DjangoFilterBackend,SearchFilter,OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'name']
    pagination_class = DefaultPagination
    permission_classes = [IsAdminOrReadOnly]
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
    permission_classes = [IsAdminOrReadOnly]

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


class CartViewSet(
    CreateModelMixin,
    RetrieveModelMixin,
    DestroyModelMixin,
    GenericViewSet):
    
    queryset = models.Cart.objects.prefetch_related('items__product').all()
    serializer_class = serializers.CartSerializer
    def get_serializer_context(self):
        return {'context' : self.request}

class CartItemViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.AddCartItemSerializer
        elif self.request.method == 'PATCH':
            return serializers.UpdateCartItemSerializer
        return serializers.CartItemSerializer

    def get_serializer_context(self):
        return {'cart_id': self.kwargs['cart_pk']}

    def get_queryset(self):
        return models.CartItem.objects.filter(cart_id=self.kwargs['cart_pk']).select_related('product')

class CustomerViewSet(ModelViewSet):
    queryset = models.Customer.objects.all()
    serializer_class = serializers.CustomerSerializer
    permission_classes = [DjangoModelPermissions]
    
    # def get_permissions(self):
    #     if self.request.method == 'GET':
    #         return [AllowAny()]
    #     return [IsAuthenticated()]
    
    @action(detail=False,methods=['GET','PUT'],permission_classes=[IsAuthenticated])
    def me(self,request):
        (customer,created) = models.Customer.objects.get_or_create(id=request.user.id)
        if request.method == 'GET' :
            serializer = serializers.CustomerSerializer(customer)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = serializers.CustomerSerializer(customer,data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        
        
        


class OrderViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']
    def get_permissions(self):
        if self.request.method in ['PATCH','DELETE']:
            return [IsAdminUser()]
        return [IsAuthenticated()]
    
    def create(self, request, *args, **kwargs):
        serializer = serializers.CreateOrderSerializer(data=request.data, context={'user_id' : self.request.user.id})
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        serializer = serializers.OrderSerializer(order)
        return Response(serializer.data)
    
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.CreateOrderSerializer
        elif self.request.method == 'PATCH':
            return serializers.UpdateOrderSerializer
        return serializers.OrderSerializer
    
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return models.Order.objects.all()
        (customer_id ,created) = models.Customer.objects.only('id').get_or_create(user_id=user.id)
        return models.Order.objects.filter(customer_id=customer_id)


