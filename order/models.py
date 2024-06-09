from django.db import models
from user.models import User
from product.models import Product

# Create your models here.

class Coupon(models.Model):
    coupon_no = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField()
    min_shop_amount = models.DecimalField(max_digits=8, decimal_places=2)
    coupon_amount = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.BooleanField(default=True)
    created_date = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.coupon_no} -- ({self.start_date}) to ({self.end_date})"
    

class Order(models.Model):
    order_date = models.DateField(auto_now_add=True)
    order_no = models.CharField(max_length=50, unique=True)
    customer = models.ForeignKey(User, related_name='cusomer_order', on_delete=models.CASCADE)
    address = models.TextField(null=True, blank=True)
    payment_type = models.CharField(max_length=15, null=True, blank=True)
    total = models.DecimalField(max_digits=8, decimal_places=2)
    vat = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    shipping = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    discount = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.order_no} - {self.order_date}"
    
    
