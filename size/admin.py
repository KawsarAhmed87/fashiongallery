from django.contrib import admin
from .models import *
# Register your models here.

class SizeAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Size, SizeAdmin)