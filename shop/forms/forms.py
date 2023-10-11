from django import forms
from django.core.exceptions import ValidationError
from shop.models import Product, Photo, Category
from multiupload.fields import MultiFileField

import json


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


class MultiProductAddForm(forms.Form):
    json_file = forms.FileField(label="Загрузите JSON файл с продуктами")

    def clean_json_file(self):
        uploaded_file = self.cleaned_data.get("json_file")
        if not uploaded_file:
            raise ValidationError("Файл не найден!")

        data_string = uploaded_file.read().decode('utf-8')
        try:
            data = json.loads(data_string)
        except json.JSONDecodeError:
            raise ValidationError("Ошибка при декодировании JSON файла!")

        for product_data in data.get('Products', []):
            # Проводим валидацию для всех полей ForeignKey
            # Для простоты я добавлю только валидацию для категории
            if not Category.objects.filter(name=product_data.get("category")).exists():
                raise ValidationError(f"Категория {product_data.get('category')} не найдена!")

            # TODO: Добавьте валидацию для остальных полей
            # Подразумевается, что в JSON файле для фотографий указаны URLы. Вы можете адаптировать это, если структура иная.

        return uploaded_file
