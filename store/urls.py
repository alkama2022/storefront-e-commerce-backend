from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter

from . import views


router = DefaultRouter()

router.register(
    "products",
    views.ProductViewSet,
    basename="product",
)

router.register(
    "collections",
    views.CollectionViewSet,
    basename="collection",
)

router.register(
    "carts",
    views.CartViewSet,
    basename="cart",
)


# /carts/<cart_pk>/items/
cart_router = NestedDefaultRouter(
    router,
    "carts",
    lookup="cart",
)

cart_router.register(
    "items",
    views.CartItemViewSet,
    basename="cart-items",
)


# /products/<product_pk>/reviews/
product_router = NestedDefaultRouter(
    router,
    "products",
    lookup="product",
)

product_router.register(
    "reviews",
    views.ReviewViewSet,
    basename="product-reviews",
)


urlpatterns = (
    router.urls
    + cart_router.urls
    + product_router.urls
)