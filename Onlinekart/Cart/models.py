from django.db import models
from Shop.models import *

from accounts.models import Account
# Create your models here.

class Cart(models.Model):
    cart_id = models.CharField(max_length=200)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.cart_id

class CartItem(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.product.product_name

    def get_total(self):
        return self.quantity * self.product.price
