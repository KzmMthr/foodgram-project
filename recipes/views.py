from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from api.models import Purchase

from .forms import RecipeEnterForm
from .models import Recipe, Tag
from .utils import get_recipes_tags, paginator_mixin, get_ingridients

User = get_user_model()


def index(request):
    recipes = get_recipes_tags(request)
    all_tags = Tag.objects.all()
    page, paginator = paginator_mixin(request, recipes)
    return render(
        request, 'indexAuth.html',
        {'page': page, 'paginator': paginator, 'all_tags': all_tags})


def recipe_view(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    return render(request, 'singlePage.html', {'recipe': recipe})


@login_required
def recipe_add(request):
    form = RecipeEnterForm(request.POST or None, files=request.FILES or None)
    if request.method == 'POST' and not get_ingridients(request):
        form.add_error(None, 'Введите хотя бы один ингридиент')
    if form.is_valid():
        recipe_save = form.save_recipe(request)
        if recipe_save == 400:
            return redirect('page_bad_request')
        return redirect('index')
    return render(
        request, 'formRecipe.html',
        {'form': form, 'title': 'Создание рецепта', 'button': 'сохранить'}
    )


@login_required
def recipe_edit(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    if request.user != recipe.author:
        return redirect('recipe_view', pk=pk)

    form = RecipeEnterForm(request.POST or None,
                           files=request.FILES or None, instance=recipe)

    if request.method == 'POST' and not get_ingridients(request):
        form.add_error(None, 'Введите хотя бы один ингридиент')

    if form.is_valid():
        for tag_id in recipe.tags.all():
            recipe.tags.remove(tag_id)
        recipe.recipe_ingredients.all().delete()
        recipe_save = form.save_recipe(request)
        if recipe_save == 400:
            return redirect('page_bad_request')
        return redirect('recipe_view', pk=pk)

    return render(request, 'formRecipe.html', {'form': form,
                                               'recipe': recipe,
                                               'title': 'Редактирование',
                                               'button': 'Сохранить',
                                               'delete': 'Удалить'}
                  )


@login_required
def recipe_remove(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    if request.user == recipe.author:
        recipe.delete()
        return redirect('profile', recipe.author)
    return redirect('index')


def profile(request, username):
    recipes = Recipe.objects.filter(author__username=username)
    page, paginator = paginator_mixin(request, recipes)
    return render(request, 'authorRecipe.html',
                  {'page': page, 'paginator': paginator})


@login_required
def favorites(request):
    recipes = get_recipes_tags(request).filter(favorites__author=request.user)
    all_tags = Tag.objects.all()
    page, paginator = paginator_mixin(request, recipes)
    return render(
        request, 'favorite.html',
        {'page': page, 'paginator': paginator, 'all_tags': all_tags})


@login_required
def subscriptions(request):
    authors = User.objects.prefetch_related('recipes').filter(
        following__follower=request.user).annotate(
        recipe_ingredients=Count('recipes__id'))
    page, paginator = paginator_mixin(request, authors)
    return render(request, 'myFollow.html',
                  {'page': page, 'paginator': paginator})


def purchases(request):
    recipes = Recipe.objects.filter(purchases__author=request.user)
    return render(request, 'shopList.html', {'recipes': recipes})


def purchase_remove(request, recipe_id):
    purchase = get_object_or_404(
        Purchase, author=request.user, recipe__id=recipe_id)
    if request.user == purchase.author:
        purchase.delete()
        return redirect('purchases')
    return redirect('index')


def purchase_count(request):
    if request.user.is_authenticated:
        return {'purchase_count': Purchase.objects.filter(author=request.user
                                                          ).count()}
    return {'purchase_count': None}


@login_required
def get_shoplist(request):
    ingredients = Recipe.objects.prefetch_related(
        'ingredients', 'recipe_ingredients').filter(
        purchases__author=request.user).order_by('ingredients__name').values(
        'ingredients__name', 'ingredients__dimension').annotate(
        count=Sum('recipe_ingredients__count'))

    ingredient_txt = [
        (f"\u2022 {item['ingredients__name'].capitalize()} "
         f"({item['ingredients__dimension']}) \u2014 {item['count']} \n")
        for item in ingredients
    ]
    filename = 'shoplist.txt'
    response = HttpResponse(ingredient_txt, content_type='text/plain')
    response['Content-Disposition'] = f'attachment; filename={filename}'
    return response
