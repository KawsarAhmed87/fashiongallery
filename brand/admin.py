from django.contrib import admin
from .models import *
# Register your models here.

class BrandAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Brand, BrandAdmin)
