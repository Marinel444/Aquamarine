from django.db import models
from common.models import Category, Subcategory, Country, Brand


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='tile_category', on_delete=models.CASCADE)
    sub_category = models.ForeignKey(Subcategory, related_name='tile_subcategory', on_delete=models.CASCADE)
    country = models.ForeignKey(Country, related_name='tile_country', on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, related_name='tile_brand', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    article = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    size = models.CharField(max_length=12, blank=True)
    color = models.CharField(max_length=100, blank=True)
    material = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return self.name


class Photo(models.Model):
    product = models.ForeignKey(Product, verbose_name='tile_product', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=f'tile/%Y/%m/%d/')
