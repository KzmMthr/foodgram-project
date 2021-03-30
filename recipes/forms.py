from django import forms

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

    # def save_recipe(self, request):
    #     '''Save recipe data'''
    #     try:
    #         with transaction.atomic():
    #             recipe = self.save(commit=False)
    #             recipe.author = request.user
    #             recipe.save()
    #             for tag in self.cleaned_data['tags']:
    #                 recipe.tags.add(tag.id)
    #
    #             ingredients = {}
    #             for key, value in self.data.items():
    #                 if 'nameIngredient' in key:
    #                     name = value
    #                 elif 'valueIngredient' in key:
    #                     count = Decimal(value.replace(',', '.'))
    #                 elif 'unitsIngredient' in key:
    #                     dimension = value
    #                     ingredient = get_object_or_404(
    #                         Ingredient, name=name, dimension=dimension)
    #                     if ingredient.name not in ingredients.keys():
    #                         ingredients[name] = [ingredient, count]
    #                     else:
    #                         ingredients[name][1] += count
    #             recipe_ingridients = []
    #             for recipe_ingridient in ingredients.values():
    #                 recipe_ingridients.append(
    #                     RecipeIngredient(
    #                         ingredient=recipe_ingridient[0],
    #                         recipe=recipe, count=recipe_ingridient[1]
    #                     )
    #                 )
    #             RecipeIngredient.objects.bulk_create(
    #                 recipe_ingridients
    #             )
    #     except IntegrityError:
    #         return 400
