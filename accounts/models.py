from django.db import models
from purchase.models import Supplier, Purchase
from order.models import Order
from item_account.models import Item_account
from user.models import User
       

class Accounts(models.Model):
    date = models.DateField()
    purchase_info = models.ForeignKey(Purchase, related_name='purchase', blank=True, null=True, on_delete=models.CASCADE)
    order_info = models.ForeignKey(Order, related_name='order', blank=True, null=True, on_delete=models.CASCADE)
    debit = models.ForeignKey(Item_account, related_name='debit_account', on_delete=models.CASCADE)
    credit = models.ForeignKey(Item_account, related_name='credit_account', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    created_by = models.ForeignKey(User, related_name='user_account', on_delete=models.CASCADE)
    created_date = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.date} - Debit: {self.purchase_info}, Credit: {self.order_info} {self.amount}"
    
    class Meta:
        ordering = ['-date']
        verbose_name = 'Account Entry'
        verbose_name_plural = 'Account Entries'