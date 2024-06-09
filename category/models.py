from django.db import models
from django.utils.text import slugify
from category.validation import validate_image
import os

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, null=True, blank=True)
    featured = models.BooleanField(default=False)
    image = models.ImageField(upload_to='category/', null=True, blank=True, validators=[validate_image])
    created_date = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        # Check if this is an update to an existing Category instance
        if self.pk:
            # Get the original instance from the database
            data = Category.objects.get(pk=self.pk)

            # Check if the profile_image field has changed
            if data.image and data.image != self.image:
                # Delete the old image file
                os.remove(data.image.path)

        super(Category, self).save(*args, **kwargs)