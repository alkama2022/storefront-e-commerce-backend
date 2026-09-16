from decimal import Decimal

from rest_framework import serializers
from .models import Product,Collection


class CollectionSeriliazer(serializers.ModelSerializer):
  class Meta:
    model = Collection
    fields = ['id','title','product_count']
    
    product_count = serializers.IntegerField()
    
class ProductSerializer(serializers.ModelSerializer):
  class Meta:
    model = Product
    fields = ['id','title','price','price_with_tax','collection']
  price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')
  
  # collection = serializers.HyperlinkedRelatedField(
  #   queryset = Product.objects.all(),
  #   view_name ='collection-detail'
  # )
  
  # collection = serializers.StringRelatedField()
  
  # collection = serializers.PrimaryKeyRelatedField(
  #     queryset = Product.objects.all()
  # )
  def calculate_tax(self, product:Product):
    return product.price * Decimal(1.06)