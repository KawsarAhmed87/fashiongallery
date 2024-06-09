from django.db import models
from django.utils.text import slugify
from unidecode import unidecode
from user.models import User
from category.models import Category
from brand.models import Brand
from tag.models import Tag
from size.models import Size
from colour.models import Colour
from product.validation import validate_image
import os

import random
import string

from django.utils.html import mark_safe

def generate_sku():
    letters = string.ascii_uppercase
    digits = string.digits
    sku = ''.join(random.choice(letters + digits) for i in range(12))
    return sku

    
class Product(models.Model):
    name = models.CharField(max_length=250, unique=True)
    sku = models.CharField(max_length=12, unique=True)
    slug = models.SlugField(unique=True, max_length=250, null=True, blank=True)
    category = models.ForeignKey(Category, related_name='category_product', on_delete=models.CASCADE, null=True, blank=True)
    tags = models.ManyToManyField(Tag, related_name='tag_product', blank=True)
    brand = models.ForeignKey(Brand, related_name='brand_product', null=True, blank=True, on_delete=models.CASCADE)
    sizes = models.ManyToManyField(Size, related_name='size_product',blank=True)
    colours = models.ManyToManyField(Colour, related_name='colour_product', blank=True)
    featured = models.BooleanField(default=False)
    purchase_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True, )
    price = models.DecimalField(max_digits=8, decimal_places=2)
    discount_price = models.DecimalField(blank=True, null=True, max_digits=8, decimal_places=2)
    quantity = models.PositiveIntegerField(blank=True, null=True)
    image =  models.ImageField(upload_to='product/', validators=[validate_image], null=True, blank=True)
    info = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True) 
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)

    class Meta:
        ordering = ['id']
    
    def __str__(self) -> str:
        return self.name
    
        
    def save(self, *args, **kwargs):
        
        if not self.sku:
            self.sku = generate_sku()
            
        if not self.slug:  # Generate slug only if it's not already set
            self.slug = slugify(unidecode(self.name))
            
        # Check if this is an update to an existing Product instance
        if self.pk:
            # Get the original instance from the database
            data = Product.objects.get(pk=self.pk)

            # Check if the profile_image field has changed
            if data.image and data.image != self.image:
                # Delete the old image file
                os.remove(data.image.path)
        super(Product, self).save(*args, **kwargs)
      
    @property
    def related(self):
        if self.category:
            return self.category.category_product.exclude(pk=self.pk).order_by('-id')[:8]
        else:
            return []
             
    def increase_quantity(self, quantity):
        if self.quantity is not None:
            self.quantity += quantity
        else:
            self.quantity = quantity
        self.save()
        return self.quantity

    def reduce_quantity(self, quantity):
        if quantity > self.quantity:
            raise ValueError("Not enough stock availab")
        self.quantity -= quantity
        self.save()
        
        

class Comment(models.Model):
    user = models.ForeignKey(User, related_name='user_comments', on_delete=models.CASCADE)
    RATING_CHOICES = (
        (1, '1 Star'),
        (2, '2 Stars'),
        (3, '3 Stars'),
        (4, '4 Stars'),
        (5, '5 Stars'),
    )
    rating =models.IntegerField(blank=True, null=True, choices=RATING_CHOICES)
    product = models.ForeignKey(Product, related_name='product_comments', on_delete=models.CASCADE)
    text = models.TextField()
    created_date = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.text
    
    def get_rating(self):
        return mark_safe('<i class="fas fa-star"></i>' * self.rating)

class Reply(models.Model):
    user = models.ForeignKey(User, related_name='user_replies', on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, related_name='comment_replies', on_delete=models.CASCADE)
    text = models.TextField()
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.text