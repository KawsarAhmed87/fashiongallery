from django.db import models
from user.models import User


# Create your models here.
class Supplier(models.Model):
    name = models.CharField(max_length=100, unique=True)
    phone = models.CharField(max_length=30, unique=True)
    email = models.EmailField(unique=True)
    bank = models.TextField()
    address = models.TextField()
    created_date = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
        

class Purchase(models.Model):
    purchase_date = models.DateField()
    purchase_no = models.CharField(max_length=50, unique=True)
    referance = models.CharField(max_length=100, null=True, blank=True)
    supplier = models.ForeignKey(Supplier, related_name='supplier_purchase', on_delete=models.CASCADE)
    total = models.CharField(max_length=12, null=True, blank=True)
    created_by = models.ForeignKey(User, related_name='user_purchase', on_delete=models.CASCADE)
    created_date = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.purchase_no} - {self.purchase_date}"
    

