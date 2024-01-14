from django.test import TestCase
from django.urls import reverse

from accounts.models import CustomUser

buyer_email = 'test_buyer@test.com'
seller_email = 'test_seller@test.com'
password = 'test_password'

buyer_profile = {'first_name':'buyer_first_name',
                 'last_name':'buyer_last_name',
                 'date_of_birth': '2000-01-01',
                 'phone': '111-1111-1111',
                 'address': 'test_address'}

buyer_update_profile = {'first_name':'buyer_update_first_name',
                        'last_name':'buyer_last_name',
                        'date_of_birth': '2000-01-01',
                        'phone': '111-1111-1111',
                        'address': 'test_address'}

seller_profile = {'first_name':'seller_first_name',
                 'last_name':'seller_last_name',
                 'date_of_birth': '1990-01-01',
                 'phone': '222-2222-2222',
                 'address': 'test_address',
                 'farm_name': 'test_farm_name'}

seller_update_profile = {'first_name':'seller_update_first_name',
                         'last_name':'seller_last_name',
                         'date_of_birth': '1990-01-01',
                         'phone': '222-2222-2222',
                         'address': 'test_address',
                         'farm_name': 'test_farm_name'}


class BuyerCreateViewTests(TestCase):
  @classmethod
  def setUpTestData(cls):
    cls.buyer = CustomUser.objects.create(email=buyer_email, is_buyer=True)
    cls.buyer.set_password(password)
    cls.buyer.save()
    
    cls.seller = CustomUser.objects.create(email=seller_email, is_seller=True)
    cls.seller.set_password(password)
    cls.seller.save()
  
  def test_buyer_create(self):
    self.client.login(email=buyer_email, password=password)
    response = self.client.post(reverse('accounts:buyer_create'), buyer_profile)
    self.assertEqual(response.url, f'/accounts/buyer_detail/{self.buyer.pk}/')
    response = self.client.get(response.url)
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, 'buyer_first_name')
    self.assertTemplateUsed(response, 'accounts/user_prof_detail.html')
    
  def test_buyer_create_by_seller(self):
    self.client.login(email=seller_email, password=password)
    response = self.client.get(reverse('accounts:buyer_create'))
    self.assertEqual(response.status_code, 403)
    
  def test_buyer_have_profile(self):
    self.buyer.is_profile = True
    self.buyer.save()
    self.client.login(email=buyer_email, password=password)
    response = self.client.get(reverse('accounts:buyer_create'))
    self.assertEqual(response.status_code, 403)
    
class BuyerDetailViewTests(TestCase):
  @classmethod
  def setUpTestData(cls):
    cls.buyer = CustomUser.objects.create(email=buyer_email, is_buyer=True)
    cls.buyer.set_password(password)
    cls.buyer.save()
    
  def test_my_page(self):
    self.client.login(email=buyer_email, password=password)
    self.client.post(reverse('accounts:buyer_create'), buyer_profile)
    response = self.client.get(reverse('accounts:buyer_detail', 
                                      kwargs={'pk': self.buyer.pk})) 
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, 'buyer_first_name')
    self.assertTemplateUsed(response, 'accounts/user_prof_detail.html')
    
  def test_not_my_page(self):
    self.client.login(email=buyer_email, password=password)
    response = self.client.get(reverse('accounts:buyer_detail', 
                                       kwargs={'pk': self.buyer.pk + 1})) 
    self.assertEqual(response.status_code, 403)
    
    
class BuyerUpdateViewTests(TestCase):
  @classmethod
  def setUpTestData(cls):
    cls.buyer = CustomUser.objects.create(email=buyer_email, is_buyer=True)
    cls.buyer.set_password(password)
    cls.buyer.save()
    
  def test_my_page(self):
    self.client.login(email=buyer_email, password=password)
    self.client.post(reverse('accounts:buyer_create'), buyer_profile)
    response = self.client.post(reverse('accounts:buyer_update',
                                        kwargs={'pk': self.buyer.pk}),
                                buyer_update_profile)
    response = self.client.get(response.url)
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, 'buyer_update_first_name')
    self.assertNotContains(response, 'buyer_first_name')
    self.assertTemplateUsed(response, 'accounts/user_prof_detail.html')
    
  def test_not_my_page(self):
    self.client.login(email=buyer_email, password=password)
    response = self.client.post(reverse('accounts:buyer_update', 
                                       kwargs={'pk': self.buyer.pk + 1}),
                                buyer_update_profile) 
    self.assertEqual(response.status_code, 403)
    
class SellerCreateViewTests(TestCase):
  @classmethod
  def setUpTestData(cls):
    cls.buyer = CustomUser.objects.create(email=buyer_email, is_buyer=True)
    cls.buyer.set_password(password)
    cls.buyer.save()
    
    cls.seller = CustomUser.objects.create(email=seller_email, is_seller=True)
    cls.seller.set_password(password)
    cls.seller.save()
    
  def test_seller_create(self):
    self.client.login(email=seller_email, password=password)
    response = self.client.post(reverse('accounts:seller_create'),
                                seller_profile)
    self.assertEqual(response.url, f'/accounts/seller_detail/{self.seller.pk}/')
    response = self.client.get(response.url)
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, 'seller_first_name')
    self.assertTemplateUsed(response, 'accounts/user_prof_detail.html')
    
  def test_seller_create_by_buyer(self):
    self.client.login(email=buyer_email, password=password)
    response = self.client.get(reverse('accounts:seller_create'))
    self.assertEqual(response.status_code, 403)
    
  def test_seller_have_profile(self):
    self.seller.is_profile = True
    self.seller.save()
    self.client.login(email=seller_email, password=password)
    response = self.client.get(reverse('accounts:seller_create'))
    self.assertEqual(response.status_code, 403)

class SellerDetailViewTests(TestCase):
  @classmethod
  def setUpTestData(cls):
    cls.seller = CustomUser.objects.create(email=seller_email, is_seller=True)
    cls.seller.set_password(password)
    cls.seller.save()
    
  def test_my_page(self):
    self.client.login(email=seller_email, password=password)
    self.client.post(reverse('accounts:seller_create'), seller_profile)
    response = self.client.get(reverse('accounts:seller_detail', 
                                       kwargs={'pk': self.seller.pk})) 
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, 'seller_first_name')
    self.assertTemplateUsed(response, 'accounts/user_prof_detail.html')


class SellerUpdateViewTests(TestCase):
  @classmethod
  def setUpTestData(cls):
    cls.seller = CustomUser.objects.create(email=seller_email, is_seller=True)
    cls.seller.set_password(password)
    cls.seller.save()
    
  def test_my_page(self):
    self.client.login(email=seller_email, password=password)
    self.client.post(reverse('accounts:seller_create'), seller_profile)
    response = self.client.post(reverse('accounts:seller_update',
                                        kwargs={'pk': self.seller.pk}),
                                seller_update_profile)
    response = self.client.get(response.url)
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, 'seller_update_first_name')
    self.assertNotContains(response, 'seller_first_name')
    self.assertTemplateUsed(response, 'accounts/user_prof_detail.html')
    
  def test_not_my_page(self):
    self.client.login(email=seller_email, password=password)
    response = self.client.post(reverse('accounts:seller_update', 
                                       kwargs={'pk': self.seller.pk + 1}),
                                seller_update_profile) 
    self.assertEqual(response.status_code, 403)