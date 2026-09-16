from django.db.models.aggregates import Count
from django.shortcuts import render,get_list_or_404
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.mixins import CreateModelMixin
from .models import Product,Collection
from .serializers import ProductSerializer,CollectionSeriliazer


class PRoductList(APIView):
  def get(self,request):
    product = Product.objects.select_related('collection').all()
    serializer = ProductSerializer(product,many=True,context={'request' : request})
    return Response(serializer.data)
    
  def post(self,request):
    serializer = ProductSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)


class ProductDetel(APIView):
  def get(self,request,id):
    product = get_list_or_404(Product,pk=id)
    serializer = ProductSerializer(product)
    return Response(serializer.data)
  def put(self,request,id):
    product = get_list_or_404(Product,pk=id)
    serializer = ProductSerializer(product,data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data) 
  def delete(self,request,id):
    product = get_list_or_404(Product,pk=id)
    if product.orderitem_set.count > 0 :
      return Response({'error':'product can not deleted becouse it is associated with an order item'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
    product.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
  
@api_view(['GET','POST'])
def collection_list(request):
  if request.method == 'GET':
    queryset = Collection.objects.annotate(product_count=Count('products'))
    serializer = CollectionSeriliazer(queryset)
    serializer.is_valid(raise_exception=True)
    return Response(serializer.data)
  
  elif request.method == 'POST' :
    serializer = CollectionSeriliazer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data,status=status.HTTP_201_CREATED)
  
@api_view(['GET','PUT','DELETE'])

def collection_detail(request,pk):
  collection = get_list_or_404(Collection.objects.annotate(product_count=Count('products')),pk=pk)
  if request.method == 'GET':
    serializer = ProductSerializer(collection)
    return Response(serializer.data)
  elif request.method == 'PUT':
    serializer = CollectionSeriliazer(collection,request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)
  elif request.method == 'DELETE' :
    if collection.products.count > 0 :
      return Response({'error' : 'Collections Can not be deleted becouse it is associated with product object'})
    return Response(status=status.HTTP_204_NO_CONTENT)