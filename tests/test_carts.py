from django.test import TestCase
from django.urls import reverse

from accounts.models import CustomUser, Buyer, Seller
from products.models import Product
from carts.models import Cart, CartItem

buyer_email = 'test_buyer@test.com'
buyer2_email = 'test_buyer2@test.com'
seller_email = 'test_seller@test.com'
password = 'test_password'

buyer_profile = {'first_name':'buyer1_first_name',
                 'last_name':'buyer1_last_name',
                 'date_of_birth': '2000-01-01',
                 'phone': '111-1111-1111',
                 'address': 'test_address'}

buyer2_profile = {'first_name':'buyer2_first_name',
                 'last_name':'buyer2_last_name',
                 'date_of_birth': '2000-01-01',
                 'phone': '111-1111-1111',
                 'address': 'test_address'}

seller_profile = {'first_name':'seller_first_name',
                 'last_name':'seller_last_name',
                 'date_of_birth': '1990-01-01',
                 'phone': '222-2222-2222',
                 'address': 'test_address',
                 'farm_name': 'test_farm_name'}

product_data1 = {'name': 'test_product1',
                 'price': 100,
                 'amount': '1個',
                 'description': 'test_description'}

product_data2 = {'name': 'test_product2',
                 'price': 300,
                 'amount': '1個',
                 'description': 'test_description'}

class AddCartitemFuncTests(TestCase):
  @classmethod
  def setUpTestData(cls):
    cls.buyer = CustomUser.objects.create(email=buyer_email, is_buyer=True)
    cls.buyer.set_password(password)
    cls.buyer.save()
    Buyer.objects.create(user=cls.buyer, **buyer_profile)
    
    cls.seller = CustomUser.objects.create(email=seller_email, is_seller=True)
    cls.seller.set_password(password)
    cls.seller.save()
    Seller.objects.create(user=cls.seller, **seller_profile)
    
    cls.product1 = Product.objects.create(seller=cls.seller.seller,
                                          **product_data1)
    cls.product2 = Product.objects.create(seller=cls.seller.seller,
                                          **product_data2)
  
  def test_create_cart_and_cartitem(self):
    self.client.login(email=buyer_email, password=password)
    self.assertEqual(Cart.objects.all().count(), 0)
    self.assertEqual(CartItem.objects.all().count(), 0)
    response = self.client.post(reverse('carts:cart_create',
                                        kwargs={'product_id': self.product1.pk}), {'amount': '1'})
    self.assertEqual(Cart.objects.all().count(), 1)
    self.assertEqual(CartItem.objects.all().count(), 1)
    response = self.client.get(response.url)
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, 'test_product1')
    self.assertContains(response, '1個')
    self.assertContains(response, '110円')
    self.assertTemplateUsed(response, 'carts/cart_detail.html')
    
  def test_add_existing_cartitem(self):
    cart = Cart.objects.create(buyer=self.buyer.buyer)
    CartItem.objects.create(cart=cart, product=self.product1, amount=1,
                            price=self.product1.price_with_tax * 1)
    self.client.login(email=buyer_email, password=password)
    self.assertEqual(Cart.objects.all().count(), 1)
    self.assertEqual(CartItem.objects.all().count(), 1)
    response = self.client.post(reverse('carts:cart_create',
                                        kwargs={'product_id': self.product1.pk}), {'amount': 2})
    self.assertEqual(Cart.objects.all().count(), 1)
    self.assertEqual(CartItem.objects.all().count(), 1)
    self.assertEqual(CartItem.objects.first().amount, 3)
    self.assertEqual(CartItem.objects.first().price, 330)
    response = self.client.get(response.url)
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, 'test_product1')
    self.assertContains(response, '3個')
    self.assertContains(response, '330円')
    self.assertTemplateUsed(response, 'carts/cart_detail.html')
    
  def test_add_new_cartitem(self):
    cart = Cart.objects.create(buyer=self.buyer.buyer)
    CartItem.objects.create(cart=cart, product=self.product1, amount=1,
                            price=self.product1.price_with_tax * 1)
    self.client.login(email=buyer_email, password=password)
    self.assertEqual(Cart.objects.all().count(), 1)
    self.assertEqual(CartItem.objects.all().count(), 1)
    response = self.client.post(reverse('carts:cart_create',
                                        kwargs={'product_id': self.product2.pk}), {'amount': 5})
    self.assertEqual(Cart.objects.all().count(), 1)
    self.assertEqual(CartItem.objects.all().count(), 2)
    self.assertEqual(CartItem.objects.get(product=self.product1).amount, 1)
    self.assertEqual(CartItem.objects.get(product=self.product1).price, 110)
    self.assertEqual(CartItem.objects.get(product=self.product2).amount, 5)
    self.assertEqual(CartItem.objects.get(product=self.product2).price, 1650)
    response = self.client.get(response.url)
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, 'test_product1')
    self.assertContains(response, '1個')
    self.assertContains(response, '110円')
    self.assertContains(response, 'test_product2')
    self.assertContains(response, '5個')
    self.assertContains(response, '1650円')
    self.assertTemplateUsed(response, 'carts/cart_detail.html')
    
class CartListViewTests(TestCase):
  @classmethod
  def setUpTestData(cls):
    cls.buyer1 = CustomUser.objects.create(email=buyer_email, is_buyer=True)
    cls.buyer1.set_password(password)
    cls.buyer1.save()
    Buyer.objects.create(user=cls.buyer1, **buyer_profile)
    
    cls.buyer2 = CustomUser.objects.create(email=buyer2_email, is_buyer=True)
    cls.buyer2.set_password(password)
    cls.buyer2.save()
    Buyer.objects.create(user=cls.buyer2, **buyer2_profile)
    
    cls.seller = CustomUser.objects.create(email=seller_email, is_seller=True)
    cls.seller.set_password(password)
    cls.seller.save()
    Seller.objects.create(user=cls.seller, **seller_profile)
    
    cls.product1 = Product.objects.create(seller=cls.seller.seller,
                                          **product_data1)
    cls.product2 = Product.objects.create(seller=cls.seller.seller,
                                          **product_data2)
  
  def test_my_cart_list(self):
    cart1 = Cart.objects.create(buyer=self.buyer1.buyer)
    CartItem.objects.create(cart=cart1, product=self.product1, amount=1,
                            price=self.product1.price_with_tax * 1)
    cart2 = Cart.objects.create(buyer=self.buyer2.buyer)
    CartItem.objects.create(cart=cart2, product=self.product2, amount=5,
                            price=self.product2.price_with_tax * 5)
    self.assertEqual(Cart.objects.all().count(), 2)
    self.assertEqual(CartItem.objects.all().count(), 2)
    
    self.client.login(email=buyer_email, password=password)
    response = self.client.get(reverse('carts:cart_detail',
                                        kwargs={'pk': self.buyer1.buyer.pk}))
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, 'test_product1')
    self.assertNotContains(response, 'test_product2')
    self.assertTemplateUsed(response, 'carts/cart_detail.html')
    
  def test_others_cart_list(self):
    cart1 = Cart.objects.create(buyer=self.buyer1.buyer)
    CartItem.objects.create(cart=cart1, product=self.product1, amount=1,
                            price=self.product1.price_with_tax * 1)
    cart2 = Cart.objects.create(buyer=self.buyer2.buyer)
    CartItem.objects.create(cart=cart2, product=self.product2, amount=5,
                            price=self.product2.price_with_tax * 5)
    self.assertEqual(Cart.objects.all().count(), 2)
    self.assertEqual(CartItem.objects.all().count(), 2)
    
    self.client.login(email=buyer_email, password=password)
    response = self.client.get(reverse('carts:cart_detail',
                                        kwargs={'pk': self.buyer2.buyer.pk}))
    self.assertEqual(response.status_code, 403)
    
    
class CartUpdateViewTests(TestCase):
  @classmethod
  def setUpTestData(cls):
    cls.buyer1 = CustomUser.objects.create(email=buyer_email, is_buyer=True)
    cls.buyer1.set_password(password)
    cls.buyer1.save()
    Buyer.objects.create(user=cls.buyer1, **buyer_profile)
    
    cls.buyer2 = CustomUser.objects.create(email=buyer2_email, is_buyer=True)
    cls.buyer2.set_password(password)
    cls.buyer2.save()
    Buyer.objects.create(user=cls.buyer2, **buyer2_profile)
    
    cls.seller = CustomUser.objects.create(email=seller_email, is_seller=True)
    cls.seller.set_password(password)
    cls.seller.save()
    Seller.objects.create(user=cls.seller, **seller_profile)
    
    cls.product1 = Product.objects.create(seller=cls.seller.seller,
                                          **product_data1)
    cls.product2 = Product.objects.create(seller=cls.seller.seller,
                                          **product_data2)
  
  def test_my_cart_update(self):
    cart1 = Cart.objects.create(buyer=self.buyer1.buyer)
    cartitem1 = CartItem.objects.create(cart=cart1, product=self.product1, 
                                        amount=1, price=self.product1.price_with_tax * 1)
    cartitem2 = CartItem.objects.create(cart=cart1, product=self.product2, 
                                        amount=5,price=self.product2.price_with_tax * 5)
    self.assertEqual(CartItem.objects.all().count(), 2)
    self.client.login(email=buyer_email, password=password)
    response = self.client.get(reverse('carts:cart_detail', 
                                       kwargs={'pk': self.buyer1.buyer.pk}))
    
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, 'test_product1')
    self.assertContains(response, '1個')
    self.assertContains(response, '110円')
    self.assertContains(response, 'test_product2')
    self.assertContains(response, '5個')
    self.assertContains(response, '1650円')
    response = self.client.post(reverse('carts:cart_update',
                                        kwargs={'pk': cartitem1.pk,
                                                'cart_id': cart1.pk}),
                                {'amount': 3})
    response = self.client.get(response.url)
    self.assertEqual(CartItem.objects.all().count(), 2)
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, 'test_product1')
    self.assertContains(response, '3個')
    self.assertContains(response, '330円')
    self.assertNotContains(response, '1個')
    self.assertNotContains(response, '110円')
    self.assertContains(response, 'test_product2')
    self.assertContains(response, '5個')
    self.assertContains(response, '1650円')
    
  def test_others_cart_update(self):
    cart1 = Cart.objects.create(buyer=self.buyer1.buyer)
    cartitem1 = CartItem.objects.create(cart=cart1, product=self.product1, 
                                        amount=1, price=self.product1.price_with_tax * 1)
    cart2 = Cart.objects.create(buyer=self.buyer2.buyer)
    cartitem2 = CartItem.objects.create(cart=cart2, product=self.product2, 
                                        amount=5,price=self.product2.price_with_tax * 5)
    self.assertEqual(Cart.objects.all().count(), 2)
    self.assertEqual(CartItem.objects.all().count(), 2)
    self.client.login(email=buyer_email, password=password)
    response = self.client.post(reverse('carts:cart_update',
                                        kwargs={'pk': cartitem2.pk,
                                                'cart_id': cart2.pk}),
                                {'amount': 3})
    self.assertEqual(response.status_code, 403)
    

class CartDeleteViewTests(TestCase):
  @classmethod
  def setUpTestData(cls):
    cls.buyer1 = CustomUser.objects.create(email=buyer_email, is_buyer=True)
    cls.buyer1.set_password(password)
    cls.buyer1.save()
    Buyer.objects.create(user=cls.buyer1, **buyer_profile)
    
    cls.buyer2 = CustomUser.objects.create(email=buyer2_email, is_buyer=True)
    cls.buyer2.set_password(password)
    cls.buyer2.save()
    Buyer.objects.create(user=cls.buyer2, **buyer2_profile)
    
    cls.seller = CustomUser.objects.create(email=seller_email, is_seller=True)
    cls.seller.set_password(password)
    cls.seller.save()
    Seller.objects.create(user=cls.seller, **seller_profile)
    
    cls.product1 = Product.objects.create(seller=cls.seller.seller,
                                          **product_data1)
    cls.product2 = Product.objects.create(seller=cls.seller.seller,
                                          **product_data2)
  
  def test_my_cart_delete(self):
    cart1 = Cart.objects.create(buyer=self.buyer1.buyer)
    cartitem1 = CartItem.objects.create(cart=cart1, product=self.product1, 
                                        amount=1, price=self.product1.price_with_tax * 1)
    cartitem2 = CartItem.objects.create(cart=cart1, product=self.product2, 
                                        amount=5,price=self.product2.price_with_tax * 5)
    self.assertEqual(CartItem.objects.all().count(), 2)
    self.client.login(email=buyer_email, password=password)
    response = self.client.get(reverse('carts:cart_detail', 
                                       kwargs={'pk': self.buyer1.buyer.pk}))
    
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, 'test_product1')
    self.assertContains(response, '1個')
    self.assertContains(response, '110円')
    self.assertContains(response, 'test_product2')
    self.assertContains(response, '5個')
    self.assertContains(response, '1650円')
    response = self.client.post(reverse('carts:cart_delete',
                                        kwargs={'pk': cartitem1.pk,
                                                'cart_id': cart1.pk}))
    response = self.client.get(response.url)
    self.assertEqual(CartItem.objects.all().count(), 1)
    self.assertEqual(response.status_code, 200)
    self.assertNotContains(response, 'test_product1')
    self.assertNotContains(response, '1個')
    self.assertNotContains(response, '110円')
    self.assertContains(response, 'test_product2')
    self.assertContains(response, '5個')
    self.assertContains(response, '1650円')
    
  def test_others_cart_update(self):
    cart1 = Cart.objects.create(buyer=self.buyer1.buyer)
    cartitem1 = CartItem.objects.create(cart=cart1, product=self.product1, 
                                        amount=1, price=self.product1.price_with_tax * 1)
    cart2 = Cart.objects.create(buyer=self.buyer2.buyer)
    cartitem2 = CartItem.objects.create(cart=cart2, product=self.product2, 
                                        amount=5,price=self.product2.price_with_tax * 5)
    self.assertEqual(Cart.objects.all().count(), 2)
    self.assertEqual(CartItem.objects.all().count(), 2)
    self.client.login(email=buyer_email, password=password)
    response = self.client.post(reverse('carts:cart_delete',
                                        kwargs={'pk': cartitem2.pk,
                                                'cart_id': cart2.pk}))
    self.assertEqual(response.status_code, 403)