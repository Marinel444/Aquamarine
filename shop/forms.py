from django import forms
from .models import Country, Brand, Product, Photo
from multiupload.fields import MultiFileField


class ProductFilterForm(forms.Form):
    country = forms.ModelChoiceField(queryset=Country.objects.all(), empty_label="Выберите страну", required=False)
    brand = forms.ModelChoiceField(queryset=Brand.objects.all(), empty_label="Выберите бренд", required=False)


class ProductAddForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

    images = MultiFileField(min_num=1, max_num=3, max_file_size=1024*1024*5)

    def save(self, commit=True):
        instance = super(ProductAddForm, self).save(commit)
        for each in self.cleaned_data['images']:
            Photo.objects.create(image=each, product=instance)

        return instance
