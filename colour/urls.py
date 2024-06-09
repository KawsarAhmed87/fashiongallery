from django.urls import path
from .views import *


urlpatterns = [
    path ('create-colour', create_colour, name="create_colour"),
    path ('list-colour', list_colour, name="list_colour"),
    path ('edit-colour/<int:id>', edit_colour, name="edit_colour"),
    path('colour/<int:pk>/delete/', delete_colour, name='delete_colour'),
    
]