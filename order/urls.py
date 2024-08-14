from django.contrib import admin
from django.urls import path
from order.views import *


urlpatterns = [
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/', cart, name='cart'),
    path('checkout/', checkout, name='checkout'),
    path('update_cart/<int:index>/', update_cart, name='update_cart'),
    path('empty-cart', clear_cart, name='clear_cart'),
    path('remove_from_cart/<int:index>/', remove_from_cart, name='remove_from_cart'),
    path('order-list', list_order, name='list_order'),
    path ('view-order/<int:id>', view_order, name="view_order"),
    path ('delete-order/<int:pk>', delete_order, name="delete_order"),
    
    path('toggle_order_status/', toggle_order_status, name='toggle_order_status'),
    
    path('pdf/<int:id>', render_pdf_download, name='render_pdf'),
    


    



]