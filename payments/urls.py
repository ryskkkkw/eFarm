from django.urls import path

from . import views

app_name = 'payments'

urlpatterns = [
  path('checkout/', views.create_checkout_session, name='create_checkout_session'),  # type: ignore
  path('checkout_success/', 
       views.PaymentSuccessView.as_view(), name='checkout_success'),
  path('checkout_cancel/', 
       views.PaymentCancelView.as_view(), name='checkout_cancel'),
  path('webhook/', views.my_webhook_view),
  path('list/', views.PaymentListView.as_view(), name='payment_list'),
]