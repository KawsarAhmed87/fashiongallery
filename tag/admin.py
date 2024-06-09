from django.contrib import admin
from .models import *
# Register your models here.

class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
TagAdmin
admin.site.register(Tag, TagAdmin)
