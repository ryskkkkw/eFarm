from django.contrib.auth.views import (
  LogoutView, PasswordChangeView, PasswordChangeDoneView, 
  PasswordResetView, PasswordResetDoneView, 
  PasswordResetConfirmView, PasswordResetCompleteView,
)
from django.urls import path, reverse_lazy
from django.views.generic import TemplateView

from . import views

app_name = 'accounts'

urlpatterns = [
  path('signup_index/', 
       TemplateView.as_view(
         template_name = 'accounts/signup_index.html'),
       name='signup_index'),
  path('signup/<str:roll>/', 
       views.UserAuthView.as_view(),
       name='signup'),
  path('signup_done/', 
       TemplateView.as_view(
         template_name = 'accounts/signup_done.html'),
       name='signup_done'),
  
  path('login/', views.UserLoginView.as_view(),
       name='login'),
  path('logout/', 
       LogoutView.as_view(
         template_name = 'accounts/logout.html'),
       name='logout'),
  
  path('password_change/', 
       PasswordChangeView.as_view(
         template_name = 'accounts/password_change.html',
         success_url = reverse_lazy('accounts:password_change_done')), 
       name='password_change'),
  path('password_change_done/', 
       PasswordChangeDoneView.as_view(
         template_name = 'accounts/password_change_done.html'), 
       name='password_change_done'),
  
  path('password_reset/', 
       PasswordResetView.as_view(
         template_name = 'accounts/password_reset.html',
         email_template_name = 'accounts/password_reset_email.txt',
         html_email_template_name = 'accounts/password_reset_email.html',
         subject_template_name = 'accounts/password_reset_subject.txt',
         success_url = reverse_lazy('accounts:password_reset_done'),
         from_email = 'test_mail_sender@eFarm.com'), 
       name='password_reset'),
  
  path('password_reset_done/', 
       PasswordResetDoneView.as_view(
         template_name = 'accounts/password_reset_done.html'), 
       name='password_reset_done'),
  
  path('password_reset_confirm/<str:uidb64>/<str:token>/',
       PasswordResetConfirmView.as_view(
         template_name = 'accounts/password_reset_confirm.html',
         success_url = reverse_lazy('accounts:password_reset_complete')), 
       name='password_reset_confirm'),
  
  path('password_reset_complete/', 
       PasswordResetCompleteView.as_view(
         template_name = 'accounts/password_reset_complete.html'), 
       name='password_reset_complete'),
  
  path('buyer_create/', 
       views.BuyerCreateView.as_view(),
       name='buyer_create'),
  path('buyer_update/<int:pk>', 
       views.BuyerUpdateView.as_view(),
       name='buyer_update'),
  path('buyer_detail/<int:pk>/', 
       views.BuyerDetailView.as_view(),
       name='buyer_detail'),
  
  path('seller_create/', 
       views.SellerCreateView.as_view(),
       name='seller_create'),
  path('seller_update/<int:pk>', 
       views.SellerUpdateView.as_view(),
       name='seller_update'),
  path('seller_detail/<int:pk>/', 
       views.SellerDetailView.as_view(),
       name='seller_detail'),
]
