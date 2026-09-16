from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


from .models import Product
from .serializers import productSerializer

@api_view()
def product_list(request):
  product = Product.objects.all()
  serializer = productSerializer(serializer.data)
  return Response('ok')

def product_detail(request,id):
  product = Product.objects.get(pk=id)
  serialize = productSerializer(product)
  return Response(serialize.data)