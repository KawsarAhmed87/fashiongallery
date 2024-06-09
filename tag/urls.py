from django.urls import path
from .views import *


urlpatterns = [
    path ('create-tag', create_tag, name="create_tag"),
    path ('list-tag', list_tag, name="list_tag"),
    path ('edit-tag/<int:id>', edit_tag, name="edit_tag"),
    path('tag/<int:pk>/delete/', delete_tag, name='delete_tag'),
    
]