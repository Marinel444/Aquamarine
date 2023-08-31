from django.shortcuts import render, redirect
from .models import *
from .forms import ProductFilterForm, ProductAddForm
from django.db.models import Q


def plumbing(request):
    category = Category.objects.all()
    return render(request, 'plumbing/plumbing.html', {'category': category})


def products(request, slug):
    form = ProductFilterForm(request.GET)
    products_item = Product.objects.filter(category__slug=slug).prefetch_related('photo_set').all()
    if form.is_valid():
        country = form.cleaned_data['country']
        brand = form.cleaned_data['brand']

        if country:
            products_item = products_item.filter(country=country)

        if brand:
            products_item = products_item.filter(manufacturer=brand)
    data = {
        'form': form,
        'products': products_item,
    }
    return render(request, 'plumbing/products.html', {'data': data})


def product_page(request, product_article):
    product = Product.objects.filter(article=product_article).prefetch_related('photo_set').first()
    return render(request, 'plumbing/product_page.html', {'product': product})


def add_post(request):
    if request.method == 'POST':
        form = ProductAddForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    form = ProductAddForm()
    return render(request, 'plumbing/add_post.html', {'form': form})
