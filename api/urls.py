from django.urls import include, path

from rest_framework.routers import DefaultRouter

from api.views import (
    FavoriteViewSet, IngredientAPIView, PurchaseViewSet, SubscribeViewSet)

router = DefaultRouter()

router.register('favorites', FavoriteViewSet)
router.register('purchases', PurchaseViewSet)
router.register('subscriptions', SubscribeViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('ingredients/', IngredientAPIView.as_view()),

]
