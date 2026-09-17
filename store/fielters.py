from django_filters.filterset import FilterSet

from store.models import Product

class ProductFilter(FilterSet):
    class Meta:
        model = Product
        fields = {
            'collection_id': ['exact'],
            'price' : ['gt', 'lt'],
        }
        

#https://youtu.be/MYQy-l-LUmA?si=WUDRM0FRDo2yj1Bu