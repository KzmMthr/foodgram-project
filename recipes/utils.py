from decimal import Decimal

from django.conf import settings
from django.core.paginator import Paginator

from django.db import IntegrityError, transaction
from django.shortcuts import get_object_or_404


from .models import Recipe, RecipeIngredient, Ingredient


def paginator_mixin(request, queryset):
    paginator = Paginator(queryset, settings.PER_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return page, paginator


def get_recipes_tags(request):
    if request.GET.getlist('tags'):
        tags = request.GET.getlist('tags')
        return Recipe.objects.prefetch_related(
            'author', 'tags'
        ).filter(tags__slug__in=tags).distinct()
    else:
        return Recipe.objects.all()


def get_ingridients(request):
    for key in request.POST:
        if key.startswith("nameIngredient"):
            return True
    return False


def save_recipe(request, form):
    '''Функция сохраняет данные при создании и редактировании рецепта.'''
    try:
        with transaction.atomic():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            for tag in form.cleaned_data['tags']:
                recipe.tags.add(tag.id)

            ingredients = []
            for key, value in form.data.items():
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
            return None
    except IntegrityError:
        return 400
