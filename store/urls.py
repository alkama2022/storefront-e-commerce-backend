
from django.urls import path

from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers

from . import views


router = DefaultRouter()

router.register(
    'products',
    views.ProductViewSet,
    basename='product'
)

router.register(
    'collections',
    views.CollectionViewSet,
    basename='collection'
)


nested_router = routers.NestedDefaultRouter(
    router,
    'products',
    lookup='product'
)

nested_router.register(
    'reviews',
    views.ReviewViewSet,
    basename='product-reviews'
)


urlpatterns = router.urls + nested_router.urls

