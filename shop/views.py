from django.shortcuts import render, redirect
from .models import *
from .forms import ProductFilterForm, ProductAddForm
from django.db.models import Q


def index(request):
    return render(request, 'shop/home.html')


def plumbing(request):
    category = Category.objects.all()
    return render(request, 'shop/plumbing.html', {'category': category})


def tile(request):
    return render(request, 'shop/tile.html')


def product_plumbing(request, slug):
    form = ProductFilterForm(request.GET)
    products = Product.objects.filter(category__slug=slug).prefetch_related('photo_set').all()
    if form.is_valid():
        country = form.cleaned_data['country']
        brand = form.cleaned_data['brand']

        if country:
            products = products.filter(country=country)

        if brand:
            products = products.filter(manufacturer=brand)
    data = {
        'form': form,
        'products': products,
    }
    return render(request, 'shop/products.html', {'data': data})


def product_page(request, product_article):
    product = Product.objects.filter(article=product_article).prefetch_related('photo_set').first()
    return render(request, 'shop/product_plumbing.html', {'product': product})


def add_post(request):
    if request.method == 'POST':
        form = ProductAddForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    form = ProductAddForm()
    return render(request, 'shop/add_post.html', {'form': form})


def search_view(request):
    query = request.GET.get('q')
    if query:
        products = Product.objects.filter(Q(name__icontains=query) | Q(article__icontains=query))
    else:
        products = Product.objects.all()
    data = {
        'products': products
    }
    return render(request, 'shop/search.html', {'data': data})
