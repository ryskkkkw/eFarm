from django.urls import path
from django.views.generic import DetailView

from . import views
from .models import Product

app_name = 'products'

urlpatterns = [
  path('create/', views.ProductCreateView.as_view(),
       name='product_create'),
  path('update/<int:pk>/', views.ProductUpdateView.as_view(),
       name='product_update'),
  path('delete/<int:pk>/', views.ProductDeleteView.as_view(),
       name='product_delete'),
  path('list/', views.ProductListView.as_view(model=Product),
       name='product_list'),
  path('detail/<int:pk>/', DetailView.as_view(model=Product),
       name='product_detail'),
] 