from decimal import Decimal

from django import forms
from django.db import IntegrityError, transaction
from django.shortcuts import get_object_or_404

from .models import Ingredient, RecipeIngredient

from .models import Recipe


class RecipeEnterForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ('title', 'description', 'image',
                  'cooking_time', 'tags')
        widgets = {
            'description': forms.Textarea(attrs={'rows': 8}),
            'tags': forms.CheckboxSelectMultiple(
                attrs={'class': 'tags__checkbox'}), }

        help_texts = {
            'title': 'Введите название рецепта.',
            'description': 'Введите описание рецепта',
            'image': 'Выберите изображение для рецепта',
            'cooking_time': 'Введите время приготовления блюда',
        }

    def save_recipe(self, request):
        '''Save recipe data'''
        try:
            with transaction.atomic():
                recipe = self.save(commit=False)
                recipe.author = request.user
                recipe.save()
                for tag in self.cleaned_data['tags']:
                    recipe.tags.add(tag.id)

                ingredients = []
                for key, value in self.data.items():
                    if 'nameIngredient' in key:
                        name = value
                    elif 'valueIngredient' in key:
                        count = Decimal(value.replace(',', '.'))
                    elif 'unitsIngredient' in key:
                        dimension = value
                        ingredient = get_object_or_404(
                            Ingredient, name=name, dimension=dimension)
                        ingredients.append(
                            RecipeIngredient(
                                ingredient=ingredient, recipe=recipe, count=count)
                        )
                RecipeIngredient.objects.bulk_create(ingredients)
        except IntegrityError:
            return 400
