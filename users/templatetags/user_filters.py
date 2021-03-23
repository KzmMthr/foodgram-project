from django import template

from api.models import Favorite, Purchase, Subscribe

try:
    from django.urls import NoReverseMatch, reverse
except ImportError:
    from django.core.urlresolvers import NoReverseMatch, reverse
register = template.Library()


@register.filter
def addclass(field, css):
    return field.as_widget(attrs={"class": css})


@register.filter
def is_favorite(value, author):
    return Favorite.objects.filter(recipe=value, author=author).exists()


@register.filter
def is_purchase(value, author):
    return Purchase.objects.filter(recipe=value, author=author).exists()


@register.filter
def is_subscribe(value, follower):
    return Subscribe.objects.filter(
        author=value, follower=follower
    ).exists()


@register.filter
def remove_from_list(obj, value):

    return obj.remove(value)


@register.simple_tag(takes_context=True)
def active(context, pattern_or_urlname):
    try:
        pattern = reverse(pattern_or_urlname)
    except NoReverseMatch:
        pattern = pattern_or_urlname
    path = context['request'].path
    if pattern == path:
        return 'nav__item_active'
    return ''


@register.filter
def get_tags(request):
    return request.getlist('tags')


@register.filter
def rebuild_tag_link(request, tag):
    request_copy = request.GET.copy()
    tags = request_copy.getlist('tags')
    if tag in tags:
        tags.remove(tag)
        request_copy.setlist('tags', tags)
    else:
        request_copy.appendlist('tags', tag)
    return request_copy.urlencode()


@register.filter
def url_with_get(request, page):
    query = request.GET.copy()
    query['page'] = page
    return query.urlencode()
