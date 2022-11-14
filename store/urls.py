from django.urls import path, include
# from rest_framework.routers import SimpleRouter
from rest_framework_nested import routers
from store import views
# from pprint import pprint

router = routers.DefaultRouter()
router.register(r"products", views.ProductViewSet, basename="products")
router.register(r"collections", views.CollectionViewSet,
                basename="collections")
router.register(r"carts", views.CartViewSet, basename="carts")


product_router = routers.NestedDefaultRouter(
    router, r'products', lookup="product")
product_router.register(r'reviews', views.ReviewViewSet,
                        basename="product-reviews")


cart_router = routers.NestedDefaultRouter(router, r"carts", lookup="cart")
cart_router.register(r'items', views.CartItemViewSet, basename="cart-items")


# urlpatterns = router.urls + product_router.urls
urlpatterns = [
    path(r'', include(router.urls)),
    path(r'', include(product_router.urls)),
    path(r'', include(cart_router.urls))
]
