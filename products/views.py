from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import (
  ListView, 
  CreateView, 
  UpdateView, 
  DeleteView,
)

from django.conf import settings

from PIL import Image

from pathlib import Path

from accounts.models import CustomUser
from .models import Product

import os
import time

class ProductCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
  model = Product
  fields = ['name', 'price', 'amount', 'image', 'description']
  
  def test_func(self):
    return self.request.user.is_seller # type: ignore
  
  def form_valid(self, form):
    user = CustomUser.objects.get(pk=self.request.user.pk)
    form.instance.seller = user.seller # type: ignore
    
    if form.instance.image:
      image = Image.open(form.instance.image)
      print(form.instance.image)
      ratio = max(400 / image.width, 300 / image.height)
      resize_size = (round(ratio * image.width), 
                     round(ratio * image.height))
      resize_image = image.resize(resize_size)
      timestamp = str(time.time())
      resize_image.save(Path(settings.MEDIA_ROOT, 
                             'product_imgs',
                             f'{timestamp}_{str(user.pk)}.jpg'))
      form.instance.image = f'product_imgs/{timestamp}_{str(user.pk)}.jpg'
      
    return super().form_valid(form)
    
  
class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
  model = Product
  fields = ['name', 'price', 'amount', 'image', 'description']
  
  def test_func(self):
    roll = self.request.user.is_seller # type: ignore
    seller = self.request.user.seller == Product.objects.get(pk=self.kwargs['pk']).seller # type: ignore
    return roll & seller 
  
  def form_valid(self, form):
    product = Product.objects.get(pk=self.kwargs['pk'])
    user = CustomUser.objects.get(pk=self.request.user.pk)
    
    if form.instance.image:
      image = Image.open(form.instance.image)
      ratio = max(400 / image.width, 300 / image.height)
      resize_size = (round(ratio * image.width), 
                    round(ratio * image.height))
      resize_image = image.resize(resize_size)
      timestamp = str(time.time())
      resize_image.save(Path(settings.MEDIA_ROOT, 
                             'product_imgs', 
                             f'{timestamp}_{str(user.pk)}.jpg'))
      form.instance.image = f'product_imgs/{timestamp}_{str(user.pk)}.jpg'
      if os.path.isfile(Path(settings.MEDIA_ROOT, 
                             str(product.image))):
        os.remove(Path(settings.MEDIA_ROOT, str(product.image)))
    
    return super().form_valid(form)


class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
  model = Product
  template_name = 'products/product_delete.html'
  success_url = reverse_lazy('products:product_list')
  
  def test_func(self):
    roll = self.request.user.is_seller # type: ignore
    seller = self.request.user.seller == self.get_object().seller # type: ignore
    return roll & seller


class ProductListView(ListView):
  model = Product
  
  def get_queryset(self):
    try:
      if self.request.user.is_seller: #type: ignore
        query = Product.objects.filter(seller__user=self.request.user)
      
        if 'search' in self.request.GET:
          words = self.request.GET['search'].split()
          
          for word in words:
            query = query & (
              Product.objects.filter(name__icontains=word) | 
              Product.objects.filter(seller__farm_name__icontains=word))
            
            if not query:
              raise ValueError('NOT Result')
          
          return query
        else:
          return query
    except:
      pass
    
    if 'search' in self.request.GET:
      words = self.request.GET['search'].split()
      
      query = Product.objects.all()
      for word in words:
        query = query & (
          Product.objects.filter(name__icontains=word) | 
          Product.objects.filter(seller__farm_name__icontains=word))
        
        if not query:
          raise ValueError('NOT Result')
      
      return query
    else:
      return super().get_queryset()