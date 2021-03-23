from django import forms
from django.utils.translation import gettext_lazy as _

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
            'title': _('Введите название рецепта.'),
            'description': _('Введите описание рецепта'),
            'image': _('Выберите изображение для рецепта'),
            'cooking_time': _('Введите время приготовления блюда'),
        }
