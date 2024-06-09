from django.urls import path
from .views import *


urlpatterns = [
    path ('create-item-account', create_item_account, name="create_item_account"),
    path ('list-item-account', list_item_account, name="list_item_account"),
    path ('edit-item-account/<int:id>', edit_item_account, name="edit_item_account"),
    path('item-account/<int:pk>/delete/', delete_item_account, name='delete_item_account'),
    
]