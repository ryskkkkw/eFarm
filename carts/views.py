from django.urls import reverse_lazy
from django.views.generic import (
  ListView, 
  UpdateView, 
  DeleteView
)
from django.shortcuts import redirect

from .models import Cart, CartItem
from products.models import Product

from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


def buyer_check(user):
  return user.is_buyer

@login_required
@user_passes_test(buyer_check)
def add_cartitem(request, product_id):
  buyer = request.user.buyer
  
  try:
    cart = Cart.objects.get(buyer=buyer)
  except:
    cart = Cart.objects.create(buyer=buyer)
    cart.save()
  
  amount = int(request.POST['amount'])
  product = Product.objects.get(pk=product_id)
  
  try:
    cartitem = cart.cartitems.get(product_id=product_id) # type: ignore
    update_amount = cartitem.amount + amount
    cart.cartitems.filter(product_id=product_id).update( # type: ignore
      amount=update_amount, 
      price=product.price_with_tax * update_amount) 
  except:
    cartitem = CartItem.objects.create(
      cart=cart,  
      product=product,
      amount=amount, 
      price=product.price_with_tax * amount
    )
    cartitem.save()
  
  return redirect('carts:cart_detail', pk=cart.buyer.pk)
  
  
class CartListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
  
  def test_func(self):
    cart = Cart.objects.filter(buyer_id=self.kwargs['pk'])
    if cart:
      return cart.first().buyer == self.request.user.buyer
    else:
      return True
    
  def get_queryset(self):
    cartitem = CartItem.objects.filter(cart__buyer_id=self.kwargs['pk'])
    return cartitem

  context_object_name = 'cartitems' 
  template_name = 'carts/cart_detail.html'
  

class CartUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
  
  def test_func(self):
    return self.request.user.buyer == Cart.objects.get(pk=self.kwargs['cart_id']).buyer # type: ignore 
  
  model = CartItem
  fields = ['amount']
  context_object_name = 'cartitem'
  template_name = 'carts/cart_update.html'
  
  def form_valid(self, form):
    super().form_valid(form)
    cartitem = CartItem.objects.get(pk=self.kwargs['pk'])
    form.instance.price = cartitem.price_with_tax
    return super().form_valid(form)
  
  def get_success_url(self):
    return reverse_lazy('carts:cart_detail', 
                        kwargs={'pk': self.kwargs['cart_id']})


class CartDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
  
  def test_func(self):
    return self.request.user.buyer == Cart.objects.get(pk=self.kwargs['cart_id']).buyer # type: ignore 
  
  model = CartItem
  context_object_name = 'cartitem'
  template_name = 'carts/cart_delete.html'
  
  def get_success_url(self):
    return reverse_lazy('carts:cart_detail', 
                        kwargs={'pk': self.kwargs['cart_id']})
  