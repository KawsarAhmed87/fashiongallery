from django.contrib import admin
from purchase.models import Purchase, Supplier

# Register your models here.
admin.site.register(Supplier)
admin.site.register(Purchase)
