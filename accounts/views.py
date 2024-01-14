from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView

from .forms import CustomUserForm  
from .models import CustomUser, Buyer, Seller


class UserAuthView(CreateView):
  model = CustomUser
  form_class = CustomUserForm
  template_name = 'accounts/signup.html'
  success_url = reverse_lazy('accounts:signup_done')
  
  def form_valid(self, form):
    if self.kwargs['roll'] == 'buyer':
      form.instance.is_buyer = True
    if self.kwargs['roll'] == 'seller':
      form.instance.is_seller = True
    return super().form_valid(form)

  
class UserLoginView(LoginView):
  template_name = 'accounts/login.html'
  
  def get_default_redirect_url(self):
    user = CustomUser.objects.get(pk=self.request.user.pk)
    
    if user.is_profile:
      return reverse('products:product_list')   
    if user.is_buyer:
      return reverse('accounts:buyer_create')
    if user.is_seller:
      return reverse('accounts:seller_create')


class BuyerCreateView(UserPassesTestMixin, CreateView):
  model = Buyer
  fields = ['first_name', 'last_name', 'date_of_birth', 
            'phone', 'address']
  template_name = 'accounts/user_prof.html'
  
  def test_func(self):
    user = CustomUser.objects.get(pk=self.request.user.pk)
    return user.is_buyer and not user.is_profile
  
  def form_valid(self, form):
    user = CustomUser.objects.get(pk=self.request.user.pk)
    form.instance.user = user
    form.save()
    user.is_profile = True
    user.save()
    return super().form_valid(form)


class BuyerUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
  model = Buyer
  fields = ['first_name', 'last_name', 'date_of_birth', 
            'phone', 'address']
  template_name = 'accounts/user_prof_update.html'
  
  def test_func(self):
    user = CustomUser.objects.get(pk=self.request.user.pk)
    return self.kwargs['pk'] == self.request.user.pk and user.is_buyer
  

class BuyerDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
  model = Buyer
  template_name = 'accounts/user_prof_detail.html'
  context_object_name = 'profile'
  
  def test_func(self):
    user = CustomUser.objects.get(pk=self.request.user.pk)
    return self.kwargs['pk'] == self.request.user.pk and user.is_buyer


class SellerCreateView(UserPassesTestMixin, CreateView): 
  model = Seller
  fields = ['first_name', 'last_name', 'date_of_birth', 'phone', 
            'address', 'farm_name', 'description', 'image']
  template_name = 'accounts/user_prof.html'
  
  def test_func(self):
    user = CustomUser.objects.get(pk=self.request.user.pk)
    return user.is_seller and not user.is_profile
  
  def form_valid(self, form):
    user = CustomUser.objects.get(pk=self.request.user.pk)
    form.instance.user = user
    form.save()
    user.is_profile = True
    user.save()
    return super().form_valid(form)
  
  
class SellerUpdateView(LoginRequiredMixin, UserPassesTestMixin,UpdateView):
  model = Seller
  fields = ['first_name', 'last_name', 'date_of_birth', 'phone', 
            'address', 'farm_name', 'description', 'image']
  template_name = 'accounts/user_prof_update.html'
  
  def test_func(self):
    user = CustomUser.objects.get(pk=self.request.user.pk)
    return self.kwargs['pk'] == self.request.user.pk and user.is_seller


class SellerDetailView(LoginRequiredMixin, DetailView):
  model = Seller
  template_name = 'accounts/user_prof_detail.html'
  context_object_name = 'profile'
  