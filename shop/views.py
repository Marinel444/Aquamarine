from django.shortcuts import render, redirect
from .models import *
from shop.forms.forms import ProductAddForm, MultiProductAddForm
from shop.forms.filters import tile_filters, plumbing_filters
from django.core.files.base import ContentFile

import json
import requests


def plumbing(request):
    category = Category.objects.filter(is_for_plumbing=True).all()
    return render(request, 'shop/plumbing.html', {'category': category})


def tile(request):
    category = Category.objects.filter(is_for_plumbing=False).all()
    return render(request, 'shop/tile.html', {'category': category})


def products(request, slug):
    products_item = Product.objects.filter(category__slug=slug).prefetch_related('photo_set').all()
    if products_item:
        if products_item[0].category.is_for_plumbing:
            form = plumbing_filters.PlumbingCategoryForm(category_slug=products_item[0].category.slug, data=request.GET)
        else:
            form = tile_filters.TileFilterForm(request.GET)
    else:
        form = None
    if form:
        if form.is_valid():
            slug = form.cleaned_data.get('category')
            if slug:
                products_item = products_item.filter(sub_category__slug=slug)
            else:
                size = form.cleaned_data.get('size')
                if size:
                    products_item = products_item.filter(size=size)
    data = {
        'form': form,
        'products': products_item,
    }
    return render(request, 'shop/products.html', {'data': data})


def product_page(request, product_article):
    product = Product.objects.filter(article=product_article).prefetch_related('photo_set').first()
    return render(request, 'shop/product_page.html', {'product': product})


def add_post(request):
    if request.method == 'POST':
        form = ProductAddForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    form = ProductAddForm()
    return render(request, 'shop/add_post.html', {'form': form})


def add_posts(request):
    if request.method == 'POST':
        form = MultiProductAddForm(request.POST, request.FILES)
        if form.is_valid():
            json_file = form.cleaned_data["json_file"]
            json_file.seek(0)
            data_string = json_file.read().decode('utf-8')
            data = json.loads(data_string)
            for product_data in data.get('Products', []):
                category = Category.objects.get(name=product_data["category"])
                sub_category = Subcategory.objects.get(name=product_data["sub_category"])
                country = Country.objects.get(name=product_data["country"])
                brand = Brand.objects.get(name=product_data["brand"])
                product = Product.objects.create(
                    category=category,
                    sub_category=sub_category,
                    country=country,
                    brand=brand,
                    name=product_data["name"],
                    article=product_data["article"],
                    description=product_data['description'],
                    size=product_data['size'],
                    color=product_data['color'],
                    material=product_data['material'],
                    stock=1,
                    price=product_data['price'],
                )

                for photo_url in product_data["photos"]:
                    response = requests.get(photo_url)
                    if response.status_code == 200:
                        file_name = photo_url.split("/")[-1]
                        photo = Photo(product=product)
                        photo.image.save(file_name, ContentFile(response.content))
                        photo.save()

            return render(request, 'shop/add_posts.html', {'form': form, 'msg': 'Товар добавлен'})

    else:
        form = MultiProductAddForm()

    return render(request, 'shop/add_posts.html', {'form': form})
