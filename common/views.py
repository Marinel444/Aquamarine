from django.shortcuts import render
from plumbing.models import Product
from .models import Category
from django.db.models import Q


def index(request):
    categories = Category.objects.all()
    return render(request, 'common/home.html', {'categories': categories})


def search_view(request):
    query = request.GET.get('q')
    if query:
        products_item = Product.objects.filter(Q(name__icontains=query) | Q(article__icontains=query))
    else:
        products_item = Product.objects.all()
    data = {
        'products': products_item
    }
    return render(request, 'common/search.html', {'data': data})