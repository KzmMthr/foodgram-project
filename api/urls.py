import debug_toolbar

from django.urls import include, path

from rest_framework.routers import DefaultRouter

from api.views import (FavoriteViewSet, IngredientAPIView, PurchaseViewSet,
                       SubscribeViewSet)

router = DefaultRouter()

router.register('favorites', FavoriteViewSet)
router.register('purchases', PurchaseViewSet)
router.register('subscriptions', SubscribeViewSet)

urlpatterns = [
    path('debug/', include(debug_toolbar.urls)),
    path('v1/', include(router.urls)),
    path('v1/ingredients/', IngredientAPIView.as_view()),

]
