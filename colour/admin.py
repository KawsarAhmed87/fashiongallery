from django.contrib import admin
from .models import *
# Register your models here.

class ColourAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Colour, ColourAdmin)
