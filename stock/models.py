from django.db import models
from product.models import Product
from purchase.models import Purchase
from order.models import Order



# Create your models here.
class Stock(models.Model):
    date = models.DateField()
    purchase = models.ForeignKey(Purchase, related_name='purchase_stock', on_delete=models.CASCADE, null=True, blank=True)
    order = models.ForeignKey(Order, related_name='order_stock', on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, related_name='product_stock', on_delete=models.CASCADE)
    quantity_in = models.PositiveIntegerField(null=True, blank=True)
    quantity_out = models.PositiveIntegerField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_date = models.DateField(auto_now_add=True)


    def __str__(self):
        return f"{self.product} - {self.date}"
    
    
    @property
    def subtotal_purchase(self):
        return self.quantity_in * self.price
    
    @property
    def subtotal_sale(self):
        return self.quantity_out * self.price
