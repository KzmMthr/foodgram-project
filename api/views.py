from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from rest_framework import filters, generics, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.models import Favorite, Purchase, Subscribe
from recipes.models import Ingredient, Recipe

from .serializers import (FavoriteSerializer, IngredientSerializer,
                          PurchaseSerializer, SubscribeSerializer)

User = get_user_model()


class CreateResponseMixin:
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response({"success": True})
        return Response({"success": False})


class IngredientAPIView(generics.ListAPIView):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['^name', ]


class SubscribeViewSet(CreateResponseMixin, viewsets.ModelViewSet):
    queryset = Subscribe.objects.all()
    serializer_class = SubscribeSerializer
    permission_classes = (IsAuthenticated,)

    def destroy(self, request, *args, **kwargs):
        author = get_object_or_404(User, pk=kwargs['pk'])
        subscribe = author.following.filter(follower=request.user)
        if subscribe.delete():
            return Response({"success": True})
        return Response({"success": False})


class FavoriteViewSet(CreateResponseMixin, viewsets.ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = (IsAuthenticated,)

    def destroy(self, request, *args, **kwargs):
        recipe = get_object_or_404(Recipe, pk=kwargs['pk'])
        favorite = recipe.favorites.filter(author=request.user)
        if favorite.delete():
            return Response({"success": True})
        return Response({"success": False})


class PurchaseViewSet(CreateResponseMixin, viewsets.ModelViewSet):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer
    permission_classes = (IsAuthenticated,)

    def destroy(self, request, *args, **kwargs):
        recipe = get_object_or_404(Recipe, pk=kwargs['pk'])
        purchase = recipe.purchases.filter(author=request.user)
        if purchase.delete():
            return Response({"success": True})
        return Response({"success": False})
