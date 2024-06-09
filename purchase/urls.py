from django.urls import path
from .views import *


urlpatterns = [
    path ('create-purchase', create_purchase, name="create_purchase"),
    path ('list-purchase', list_purchase, name="list_purchase"),
    path ('view-purchase/<int:id>', view_purchase, name="view_purchase"),
    path ('delete-purchase/<int:pk>', delete_purchase, name="delete_purchase"),
    
]