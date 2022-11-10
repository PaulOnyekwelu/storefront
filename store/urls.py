from django.urls import path
from rest_framework.routers import DefaultRouter
from store import views
from pprint import pprint

router = DefaultRouter()
router.register("products", views.ProductViewSet)
router.register("collections", views.CollectionViewSet)

urlpatterns = router.urls
