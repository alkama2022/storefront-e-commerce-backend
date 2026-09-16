from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.PRoductList.as_view()),
    path('products/<int:id>/',views.ProductDetel.as_view()),
    path('collections/',views.collection_list),
    path('collections/<int:id>/',views.collection_detail,name ='collection-detail'),
]