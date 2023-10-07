from django.shortcuts import render, redirect
from .models import *
from shop.forms.forms import ProductAddForm
from shop.forms.filters import tile_filters, plumbing_filters


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
