from django.contrib import admin

from .models import Favorite, Purchase, Subscribe


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('author', 'recipe', )
    autocomplete_fields = ('author', 'recipe', )


@admin.register(Subscribe)
class SubscribeAdmin(admin.ModelAdmin):
    list_display = ('author', 'follower', )
    autocomplete_fields = ('author', 'follower', )


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('author', 'recipe', )
    autocomplete_fields = ('author', 'recipe', )
