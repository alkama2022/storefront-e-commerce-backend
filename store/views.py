from itertools import product

from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


from .models import Product,Collection
from .serializers import productSerializer

@api_view()
def product_list(request):
  product = Product.objects.select_related('collection').all()
  serializer = productSerializer(product,context={'request' : request})
  return Response(serializer.data)

@api_view()
def product_detail(request,pk):
  product = Product.objects.get(pk=pk)
  serialize = productSerializer(product)
  return Response(serialize.data)


@api_view()
def collection_detail(request,pk):
  collection = Collection.objects.get(pk=pk)
  serialize = productSerializer(collection)
  return Response(serialize.data)