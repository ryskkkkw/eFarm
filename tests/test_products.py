from PIL import Image as img
from pathlib import Path
import time

from config import settings

from django.test import TestCase
from django.urls import reverse

from accounts.models import CustomUser
from accounts.models import Seller
from accounts.models import Buyer
from products.models import Product

email = 'test@test.com'
password = 'password'

def create_buyer():
  user = CustomUser.objects.create(email=email, is_buyer=True)
  user.set_password(password)
  user.save()
  return user

def create_seller():
  user = CustomUser.objects.create(email=email, is_seller=True)
  user.set_password(password)
  user.save()
  return user


seller1_email = 'test_seller1@test.com'
seller2_email = 'test_seller2@test.com'
buyer_email = 'test_buyer@test.com'
password = 'test_password'

seller1_profile = {'first_name': 'seller1_first_name',
                 'last_name': 'seller1_last_name',
                 'date_of_birth': '1990-01-01',
                 'phone': '222-2222-2222',
                 'address': 'test_address',
                 'farm_name': 'test_farm_name'}

seller2_profile = {'first_name': 'seller2_first_name',
                   'last_name': 'seller2_last_name',
                   'date_of_birth': '1990-01-01',
                   'phone': '222-2222-2222',
                   'address': 'test_address',
                   'farm_name': 'test_farm_name'}

buyer_profile = {'first_name': 'buyer_first_name',
                 'last_name': 'buyer_last_name',
                 'date_of_birth': '2000-01-01',
                 'phone': '111-1111-1111',
                 'address': 'test_address'}

product_data = {'price': 100,
                'amount': '1個',
                'description': 'test_description'}

product_data_with_name = {'name': 'test_product',
                          'price': 100,
                          'amount': '1個',
                          'description': 'test_description'}


class ProductCreateViewTests(TestCase):
  @classmethod
  def setUpTestData(cls):
    cls.seller = CustomUser.objects.create(email=seller1_email, is_seller=True)
    cls.seller.set_password(password)
    cls.seller.save()
    
    cls.buyer = CustomUser.objects.create(email=buyer_email, is_buyer=True)
    cls.buyer.set_password(password)
    cls.buyer.save()
  
  def test_create_product_by_seller(self):
    self.client.login(email=seller1_email, password=password)
    self.client.post(reverse('accounts:seller_create'), seller1_profile)

    with open('tests/test1.jpg', 'rb') as f:
      product_data_with_name['seller'] = self.seller.seller
      product_data_with_name['image'] = f
      response = self.client.post(reverse('products:product_create'),
                                  product_data_with_name)
      response = self.client.get(response.url)
      self.assertEqual(response.status_code, 200)
      self.assertContains(response, 'test_product')
      self.assertTemplateUsed(response, 'products/product_detail.html')

    product = Product.objects.all().first()
    img_path = Path(settings.MEDIA_ROOT, str(product.image))
    self.assertTrue(Path.exists(img_path))
    time.sleep(2)
    Path.unlink(img_path)
    
  def test_create_product_by_buyer(self):
    self.client.login(email=buyer_email, password=password)
    self.client.post(reverse('accounts:buyer_create'), buyer_profile)
  
    with open('tests/test1.jpg', 'rb') as f:
      product_data_with_name['seller'] = self.buyer.buyer
      product_data_with_name['image'] = f
      response = self.client.post(reverse('products:product_create'),
                                  product_data_with_name)
      self.assertEqual(response.status_code, 403)
  
      
class ProductUpdateViewTests(TestCase):
  @classmethod
  def setUpTestData(cls):
    cls.seller = CustomUser.objects.create(email=seller1_email, is_seller=True)
    cls.seller.set_password(password)
    cls.seller.save()
    
    cls.buyer = CustomUser.objects.create(email=buyer_email, is_buyer=True)
    cls.buyer.set_password(password)
    cls.buyer.save()
      
  def test_update_product(self):
    self.client.login(email=seller1_email, password=password)
    self.client.post(reverse('accounts:seller_create'), seller1_profile)
    
    with open('tests/test1.jpg', 'rb') as f1:
      product_data_with_name['seller'] = self.seller.seller
      product_data_with_name['image'] = f1
      self.client.post(reverse('products:product_create'), 
                       product_data_with_name)
      product1 = Product.objects.all().first()
      img_path1 = Path(settings.MEDIA_ROOT, str(product1.image))
      self.assertTrue(Path.exists(img_path1))
    
    time.sleep(2)
    with open('tests/test2.jpg', 'rb') as f2:
      update_product_data = product_data_with_name
      update_product_data['name'] = 'test_update_product'
      update_product_data['image'] = f2
      response = self.client.post(reverse('products:product_update', 
                                          kwargs={'pk': product1.pk}),  update_product_data)
      response = self.client.get(response.url)
      self.assertEqual(response.status_code, 200)
      self.assertContains(response, 'test_update_product')
      self.assertNotContains(response, 'test_product')
      self.assertTemplateUsed(response, 'products/product_detail.html')
      
    product2 = Product.objects.all().first()
    img_path2 = Path(settings.MEDIA_ROOT, str(product2.image))
    self.assertFalse(Path.exists(img_path1))
    self.assertTrue(Path.exists(img_path2))
    self.assertNotEqual(img_path1, img_path2)
    time.sleep(2)
    Path.unlink(img_path2)
  
  def test_update_product_by_other_seller(self):
    self.client.login(email=seller1_email, password=password)
    self.client.post(reverse('accounts:seller_create'), seller1_profile)
    
    with open('tests/test1.jpg', 'rb') as f1:
      product_data_with_name['seller'] = self.seller.seller
      product_data_with_name['image'] = f1
      self.client.post(reverse('products:product_create'), 
                       product_data_with_name)
      product1 = Product.objects.all().first()
      img_path1 = Path(settings.MEDIA_ROOT, str(product1.image))
      self.assertTrue(Path.exists(img_path1))
    
    self.client.logout()
    time.sleep(2)
    
    with open('tests/test2.jpg', 'rb') as f2:
      other_sellser = CustomUser.objects.create_user(
        email=seller2_email, password=password
      )
      other_sellser.is_seller = True
      other_sellser.save()
      self.client.login(email=seller2_email, password=password)
      self.client.post(reverse('accounts:seller_create'), seller2_profile)
      update_product_data = product_data_with_name
      update_product_data['name'] = 'test_update_product'
      update_product_data['image'] = f2
      response = self.client.post(reverse('products:product_update', 
                                          kwargs={'pk': product1.pk}),  update_product_data)
      self.assertEqual(response.status_code, 403)
      
    self.assertTrue(Path.exists(img_path1))
    Path.unlink(img_path1)


class ProductListViewTests(TestCase):
  @classmethod
  def setUpTestData(cls):
    cls.seller1 = CustomUser.objects.create(email=seller1_email, is_seller=True)
    cls.seller1.set_password(password)
    cls.seller1.save()
    Seller.objects.create(user=cls.seller1, **seller1_profile)
    
    cls.seller2 = CustomUser.objects.create(email=seller2_email, is_seller=True)
    cls.seller2.set_password(password)
    cls.seller2.save()
    Seller.objects.create(user=cls.seller2, **seller2_profile)
    
    cls.buyer = CustomUser.objects.create(email=buyer_email, is_buyer=True)
    cls.buyer.set_password(password)
    cls.buyer.save()
    Buyer.objects.create(user=cls.buyer, **buyer_profile)
    
    cls.seller1_product = Product.objects.create(name='seller1_product',
                                                 seller=cls.seller1.seller,
                                                 **product_data)
    cls.seller1_product = Product.objects.create(name='seller1_new_product',
                                                 seller=cls.seller1.seller,
                                                 **product_data)
    cls.seller2_product = Product.objects.create(name='seller2_product',
                                                 seller=cls.seller2.seller,
                                                 **product_data)
    cls.seller2_product = Product.objects.create(name='seller2_new_product',
                                                 seller=cls.seller2.seller,
                                                 **product_data)
    
    
  def test_product_list_seller1(self):
    self.client.login(email=seller1_email, password=password)
    response = self.client.get(reverse('products:product_list'))
    self.assertContains(response, 'Product Create')
    self.assertContains(response, 'seller1_product')
    self.assertContains(response, 'seller1_new_product')
    self.assertNotContains(response, 'seller2_product')
    self.assertNotContains(response, 'seller2_new_product')
    self.assertTemplateUsed(response, 'products/product_list.html')
    
    
  def test_product_list_seller1_with_search(self):
    self.client.login(email=seller1_email, password=password)
    response_search_seller1 = self.client.get(reverse('products:product_list'),
                                              {'search': 'seller1'})
    self.assertContains(response_search_seller1, 'Product Create')
    self.assertContains(response_search_seller1, 'seller1_product')
    self.assertContains(response_search_seller1, 'seller1_new_product')
    self.assertNotContains(response_search_seller1, 'seller2_product')
    self.assertNotContains(response_search_seller1, 'seller2_new_product')
    self.assertTemplateUsed(response_search_seller1, 
                            'products/product_list.html')
    
    response_search_new = self.client.get(reverse('products:product_list'),
                                          {'search': 'new'})
    self.assertContains(response_search_new, 'Product Create')
    self.assertContains(response_search_new, 'seller1_new_product')
    self.assertNotContains(response_search_new, 'seller1_product')
    self.assertNotContains(response_search_new, 'seller2_product')
    self.assertNotContains(response_search_new, 'seller2_new_product')
    self.assertTemplateUsed(response_search_new, 
                            'products/product_list.html')
    
  def test_product_list_seller2(self):
    self.client.login(email=seller2_email, password=password)
    response = self.client.get(reverse('products:product_list'))
    self.assertContains(response, 'Product Create')
    self.assertContains(response, 'seller2_product')
    self.assertContains(response, 'seller2_new_product')
    self.assertNotContains(response, 'seller1_product')
    self.assertNotContains(response, 'seller1_new_product')
    self.assertTemplateUsed(response, 'products/product_list.html')
    
  def test_product_list_seller2_with_search(self):
    self.client.login(email=seller2_email, password=password)
    response_search_seller2 = self.client.get(reverse('products:product_list'),
                                              {'search': 'seller2'})
    self.assertContains(response_search_seller2, 'Product Create')
    self.assertContains(response_search_seller2, 'seller2_product')
    self.assertContains(response_search_seller2, 'seller2_new_product')
    self.assertNotContains(response_search_seller2, 'seller1_product')
    self.assertNotContains(response_search_seller2, 'seller1_new_product')
    self.assertTemplateUsed(response_search_seller2, 
                            'products/product_list.html')
    
    response_search_new = self.client.get(reverse('products:product_list'),
                                          {'search': 'new'})
    self.assertContains(response_search_new, 'Product Create')
    self.assertContains(response_search_new, 'seller2_new_product')
    self.assertNotContains(response_search_new, 'seller2_product')
    self.assertNotContains(response_search_new, 'seller1_product')
    self.assertNotContains(response_search_new, 'seller1_new_product')
    self.assertTemplateUsed(response_search_new, 
                            'products/product_list.html')
    
  def test_product_list_buyer(self):
    self.client.login(email=buyer_email, password=password)
    response = self.client.get(reverse('products:product_list'))
    self.assertNotContains(response, 'Product Create')
    self.assertContains(response, 'seller1_product')
    self.assertContains(response, 'seller1_new_product')
    self.assertContains(response, 'seller2_product')
    self.assertContains(response, 'seller2_new_product')
    self.assertTemplateUsed(response, 'products/product_list.html')
    
  def test_product_list_buyer_with_search(self):
    self.client.login(email=buyer_email, password=password)
    response_search_seller2 = self.client.get(reverse('products:product_list'),
                                              {'search': 'seller2'})
    self.assertNotContains(response_search_seller2, 'Product Create')
    self.assertContains(response_search_seller2, 'seller2_product')
    self.assertContains(response_search_seller2, 'seller2_new_product')
    self.assertNotContains(response_search_seller2, 'seller1_product')
    self.assertNotContains(response_search_seller2, 'seller1_new_product')
    self.assertTemplateUsed(response_search_seller2,
                            'products/product_list.html')
    
    response_search_new = self.client.get(reverse('products:product_list'),
                                          {'search': 'new'})
    self.assertNotContains(response_search_new, 'Product Create')
    self.assertContains(response_search_new, 'seller2_new_product')
    self.assertNotContains(response_search_new, 'seller2_product')
    self.assertContains(response_search_new, 'seller1_new_product')
    self.assertNotContains(response_search_new, 'seller1_product')
    self.assertTemplateUsed(response_search_new,
                            'products/product_list.html')
    
    response_search_seller1_new = self.client.get(reverse
                                                  ('products:product_list'),{'search': 'seller1 new'})
    self.assertNotContains(response_search_seller1_new, 'Product Create')
    self.assertNotContains(response_search_seller1_new, 'seller1_product')
    self.assertContains(response_search_seller1_new, 'seller1_new_product')
    self.assertNotContains(response_search_seller1_new, 'seller2_product')
    self.assertNotContains(response_search_seller1_new, 'seller2_new_product')
    self.assertTemplateUsed(response_search_seller1_new, 
                            'products/product_list.html')
    
  def test_product_list_anonymoususer(self):
    response = self.client.get('')
    self.assertNotContains(response, 'Product Create')
    self.assertContains(response, 'seller1_product')
    self.assertContains(response, 'seller1_new_product')
    self.assertContains(response, 'seller2_product')
    self.assertContains(response, 'seller2_new_product')
    self.assertTemplateUsed(response, 'products/product_list.html')
  
  def test_product_list_anonymoususer_with_search(self):
    response_search_seller2 = self.client.get('', {'search': 'seller2'})
    self.assertNotContains(response_search_seller2, 'Product Create')
    self.assertContains(response_search_seller2, 'seller2_product')
    self.assertContains(response_search_seller2, 'seller2_new_product')
    self.assertNotContains(response_search_seller2, 'seller1_product')
    self.assertNotContains(response_search_seller2, 'seller1_new_product')
    self.assertTemplateUsed(response_search_seller2,
                            'products/product_list.html')
    
    response_search_new = self.client.get('', {'search': 'new'})
    self.assertNotContains(response_search_new, 'Product Create')
    self.assertContains(response_search_new, 'seller2_new_product')
    self.assertNotContains(response_search_new, 'seller2_product')
    self.assertContains(response_search_new, 'seller1_new_product')
    self.assertNotContains(response_search_new, 'seller1_product')
    self.assertTemplateUsed(response_search_new,
                            'products/product_list.html')
    
    response_search_seller1_new = self.client.get('',
                                                  {'search': 'seller1 new'})
    self.assertNotContains(response_search_seller1_new, 'Product Create')
    self.assertNotContains(response_search_seller1_new, 'seller1_product')
    self.assertContains(response_search_seller1_new, 'seller1_new_product')
    self.assertNotContains(response_search_seller1_new, 'seller2_product')
    self.assertNotContains(response_search_seller1_new, 'seller2_new_product')
    self.assertTemplateUsed(response_search_seller1_new, 
                            'products/product_list.html')