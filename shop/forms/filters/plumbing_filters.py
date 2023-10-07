from django import forms
from shop.models import Subcategory


class PlumbingCategoryForm(forms.Form):
    SIZE_CHOICES = [('', 'Выберите категорию')]

    def __init__(self, category_slug, *args, **kwargs):
        super(PlumbingCategoryForm, self).__init__(*args, **kwargs)
        subcategories = Subcategory.objects.filter(category__slug=category_slug)
        self.fields['category'].choices += [(sub.slug, sub.name) for sub in subcategories]

    category = forms.ChoiceField(choices=SIZE_CHOICES, required=False, label='Предназначения')
