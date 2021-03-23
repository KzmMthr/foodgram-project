from django.urls import path

from . import views

urlpatterns = [
    path('view/<int:pk>/', views.recipe_view, name='recipe_view'),
    path('edit/<int:pk>/', views.recipe_edit, name='recipe_edit'),
    path('delete/<int:pk>/', views.recipe_remove, name='recipe_remove'),
    path('author/<str:username>/', views.profile, name='profile'),
    path('subscriptions/', views.subscriptions, name='subscriptions'),
    path(
        'purchases/<int:recipe_id>/delete/', views.purchase_remove,
        name='purchase_remove'),
    path('purchases/', views.purchases, name='purchases'),
    path('favorites/', views.favorites, name='favorites'),
    path('shoplist/', views.get_shoplist, name='shoplist'),
    path('add/', views.recipe_add, name='recipe_add'),
    path('', views.index, name='index'), ]
