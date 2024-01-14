from django.db import models

from accounts.models import Buyer
from products.models import Product


class Cart(models.Model):
  buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE,
                            related_name='carts')
  created_at = models.DateTimeField(auto_now=True)
  
  class Meta:
    db_table = 'cart'
  
  def __str__(self):
    return f'buyer: {self.buyer}'

  
class CartItem(models.Model):
  cart = models.ForeignKey(Cart, on_delete=models.CASCADE,
                           related_name='cartitems')
  product = models.ForeignKey(Product, on_delete=models.CASCADE, db_index=False)
  amount = models.IntegerField(default=1)
  price = models.IntegerField(blank=True, null=True)
  
  class Meta:
    db_table = 'cartitem'
  
  def __str__(self):
    return f'buyer: {self.cart.buyer} product: {self.product}, price: {self.price} name: {self.product.name}'
  
  tax = 0.1
  
  @property
  def tax_amount(self):
    return int(self.product.price * self.amount * self.tax)
  
  @property
  def price_with_tax(self):
    return int(self.product.price * (1 + self.tax) * self.amount)