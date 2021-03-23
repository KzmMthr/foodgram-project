from django.contrib.auth import get_user_model
from django.db import models

from recipes.models import Recipe

User = get_user_model()


class Favorite(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='автор',
        related_name='favorites')
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, verbose_name='рецепт',
        related_name='favorites')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'recipe'],
                name='unique_favorites')]
        verbose_name = 'избранный'
        verbose_name_plural = 'избранные'


class Subscribe(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='following', verbose_name='автор')
    follower = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='follower',
        verbose_name='подписчик')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'follower'],
                name='unique_subscribes')]
        verbose_name = 'подписка'
        verbose_name_plural = 'подписки'


class Purchase(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='автор',
        related_name='purchases')
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, verbose_name='рецепт',
        related_name='purchases')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'recipe'],
                name='unique_purchases')]
        verbose_name = 'список покупок'
        verbose_name_plural = 'списки покупок'
