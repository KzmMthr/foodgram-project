from django.contrib.auth import get_user_model
from django.db import models

from model_utils.fields import AutoCreatedField
from model_utils.models import TimeStampedModel

User = get_user_model()


class Tag(TimeStampedModel):
    name = models.CharField(verbose_name='тег', max_length=50)
    slug = models.SlugField(max_length=20)
    color = models.CharField(verbose_name='цвет чекбокса', max_length=20)

    class Meta:
        ordering = ['id']
        verbose_name = 'тег'
        verbose_name_plural = 'теги'

    def __str__(self):
        return self.name


class Ingredient(TimeStampedModel):
    name = models.CharField(verbose_name='название',
                            max_length=250, db_index=True)
    dimension = models.CharField(
        verbose_name='единица измерения', max_length=50)

    class Meta:
        ordering = ['name']
        verbose_name = 'ингредиент'
        verbose_name_plural = 'ингредиенты'

    def __str__(self):
        return self.name


class Recipe(TimeStampedModel):
    title = models.CharField(verbose_name='название',
                             max_length=250, db_index=True)
    description = models.TextField(verbose_name='описание')
    image = models.ImageField(verbose_name='картинка', upload_to='upload')
    cooking_time = models.IntegerField(
        verbose_name='время приготовления в минутах')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='автор',
        related_name='recipe', db_index=True)
    ingredients = models.ManyToManyField(
        Ingredient, through='RecipeIngredient')
    tags = models.ManyToManyField(Tag, related_name='recipes')

    class Meta:
        verbose_name = 'рецепт'
        verbose_name_plural = 'рецепты'
        ordering = ['-created']

    def __str__(self):
        return self.title


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe, verbose_name='рецепт', on_delete=models.CASCADE,
        related_name='recipe_ingredients')
    ingredient = models.ForeignKey(
        Ingredient, verbose_name='ингредиент', on_delete=models.CASCADE)
    cnt = models.IntegerField(verbose_name='количество')
    created = AutoCreatedField(verbose_name='дата создания')

    class Meta:
        verbose_name = 'ингредиент рецепта'
        verbose_name_plural = 'ингредиенты рецепта'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='recipe_ingredients')]
