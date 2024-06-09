from django.urls import path
from .views import *


urlpatterns = [
    path ('create-product', create_product, name="create_product"),
    path ('list-product', list_product, name="list_product"),
    path ('view-product/<int:id>/<slug:slug>', view_product, name="view_product"),
    path ('edit-product/<int:id>//<slug:slug>', edit_product, name="edit_product"),
    path('product/<int:pk>/delete/', delete_product, name='delete_product'),
    
     path ('comment-review/<int:id>', comment_review, name="comment_review"),
     path ('reply-comment/<int:id>', reply_comment, name="reply_comment"),
    
]