from django.shortcuts import render
from common.models import Category


def tile(request):
    category = Category.objects.filter(is_for_plumbing=False).all()
    return render(request, 'tile/tile.html', {'category': category})
