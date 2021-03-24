from django.conf import settings
from django.core.paginator import Paginator


def paginator_mixin(request, queryset):
    paginator = Paginator(queryset, settings.PER_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return page, paginator

def get_tags(request):
    return request.GET.getlist('tags')