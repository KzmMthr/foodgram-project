from django.conf import settings
from django.core.paginator import Paginator

from .models import Recipe


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
