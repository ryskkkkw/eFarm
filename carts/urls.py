from django.urls import path

from . import views

app_name = 'carts'

urlpatterns = [
  path('create/<int:product_id>', views.add_cartitem, name='cart_create'),
  path('detail/<int:pk>', views.CartListView.as_view(), name='cart_detail'),
  path('update/<int:pk>/<int:cart_id>', views.CartUpdateView.as_view(), name='cart_update'),
  path('delete/<int:pk>/<int:cart_id>', views.CartDeleteView.as_view(), name='cart_delete'),
]
