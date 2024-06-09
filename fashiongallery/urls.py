from django.contrib import admin
from django.urls import path, include
from .views import *

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', home, name="home"),
    path('product-details/<slug:slug>', product_details, name="product_details"),
    path('all-products', all_products, name="all_products"),
    path('category-products/<slug:slug>/', category_products, name='category_products'),
    path('search', product_search, name='product_search'),

    path('dashboard', dashboard, name="dashboard"),
    path('', include('user.urls')),
    path('', include('category.urls')),
    path('', include('brand.urls')),
    path('', include('tag.urls')),
    path('', include('size.urls')),
    path('', include('colour.urls')),
    path('', include('product.urls')),
    path('', include('item_account.urls')),
    path('', include('purchase.urls')),
    path('', include('order.urls')),
    path('', include('group.urls')),
    path('', include('role.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)