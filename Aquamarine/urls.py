"""
URL configuration for Aquamarine project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from plumbing.views import *
from tile.views import *
from common.views import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='home'),
    path('santehnika/', plumbing, name='plumbing'),
    path('add_post/', add_post, name='add_post'),
    path('search/', search_view, name='search_view_name'),
    path('plitka/', tile, name='tile'),
    re_path(r'santehnika/(?P<slug>[\w-]+)/$', products, name='plumbing_item'),
    re_path(r'(?P<product_article>[\w\d-]+)/$', product_page, name='product'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
