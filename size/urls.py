from django.urls import path
from .views import *


urlpatterns = [
    path ('create-size', create_size, name="create_size"),
    path ('list-size', list_size, name="list_size"),
    path ('edit-size/<int:id>', edit_size, name="edit_size"),
    path('size/<int:pk>/delete/', delete_size, name='delete_size'),
    
]