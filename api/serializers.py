from django.contrib.auth import get_user_model

from rest_framework import serializers

from api.models import Favorite, Purchase, Subscribe
from recipes.models import Ingredient, Recipe

User = get_user_model()


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Ingredient


class FavoriteSerializer(serializers.ModelSerializer):
    id = serializers.SlugRelatedField(
        slug_field='id', queryset=Recipe.objects.all(), source='recipe')
    author = serializers.PrimaryKeyRelatedField(
        read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        fields = ('id', 'author')
        model = Favorite

    def create(self, validated_data):
        if 'author' not in validated_data:
            validated_data['author'] = self.context['request'].user
        return Favorite.objects.create(**validated_data)


class SubscribeSerializer(serializers.ModelSerializer):
    id = serializers.SlugRelatedField(
        slug_field='id', queryset=User.objects.all(), source='author')
    follower = serializers.PrimaryKeyRelatedField(
        read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        fields = ['id', 'follower']
        model = Subscribe

    def create(self, validated_data):
        if 'follower' not in validated_data:
            validated_data['follower'] = self.context['request'].user
        return Subscribe.objects.create(**validated_data)


class PurchaseSerializer(serializers.ModelSerializer):
    id = serializers.SlugRelatedField(
        slug_field='id', queryset=Recipe.objects.all(), source='recipe')
    author = serializers.PrimaryKeyRelatedField(
        read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        fields = ('id', 'author')
        model = Purchase

    def create(self, validated_data):
        if 'author' not in validated_data:
            validated_data['author'] = self.context['request'].user
        return Purchase.objects.create(**validated_data)
