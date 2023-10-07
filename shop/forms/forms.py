from django import forms
from shop.models import Product, Photo, Subcategory
from multiupload.fields import MultiFileField


class ProductAddForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

    images = MultiFileField(min_num=1, max_num=3, max_file_size=1024 * 1024 * 5)

    def save(self, commit=True):
        instance = super(ProductAddForm, self).save(commit)
        for each in self.cleaned_data['images']:
            Photo.objects.create(image=each, product=instance)

        return instance
