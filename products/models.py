from django.db import models
from django.urls import reverse

from accounts.models import Seller


class Product(models.Model):
  name = models.CharField(max_length=50)
  price = models.IntegerField('price without tax')
  amount = models.CharField(max_length=30, default='1個')
  description = models.TextField(blank=True, null=True)
  seller = models.ForeignKey(Seller, on_delete=models.CASCADE,
                             related_name='products')
  image = models.ImageField(upload_to='product_imgs/',
                          blank=True, null=True)
  
  class Meta:
    db_table = 'product'
  
  def __str__(self):
    return f'product_name:{self.name} seller:{self.seller}'
  
  def get_absolute_url(self):
    return reverse('products:product_detail',
                   kwargs={'pk': self.pk})
  
  tax = 0.1
    
  @property
  def price_with_tax(self):
    return int(self.price * (1 + self.tax))
  