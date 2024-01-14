from django.db import models

from accounts.models import Buyer


class Payment(models.Model):
  buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE, 
                            related_name='payments')
  price = models.IntegerField('payment total price')
  shipping_name = models.CharField(max_length=100)
  shipping_postal_code = models.CharField(max_length=20)
  shipping_state = models.CharField(max_length=20)
  shipping_city = models.CharField(max_length=100)
  shipping_line1 = models.CharField(max_length=100)
  shipping_line2 = models.CharField(max_length=100, 
                                    null=True, blank=True)
  created_at = models.DateTimeField(auto_now_add=True)
  
  class Meta:
    db_table = 'payment'
  
  def __str__(self):
    return f'buyer: {self.buyer}, created_at: {self.created_at}'


class PaymentItem(models.Model):
  payment = models.ForeignKey(Payment, on_delete=models.CASCADE,
                              related_name='paymentitems')
  product = models.CharField(max_length=50)
  unit_price = models.IntegerField()
  amount = models.IntegerField()
  total_price = models.IntegerField()
  
  class Meta:
    db_table = 'paymentitem'
    
  def __str__(self):
    return f'buyer: {self.payment.buyer}, product: {self.product}, amount: {self.amount}, unit_price: {self.unit_price}, total_price: {self.total_price}'