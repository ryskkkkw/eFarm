from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.urls import reverse

from django.conf import settings


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(
            email=email,
            password=password
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
  email = models.EmailField(max_length=250, unique=True)
  is_active = models.BooleanField(default=True)
  is_admin = models.BooleanField(default=False)
  is_buyer = models.BooleanField(default=False)
  is_seller = models.BooleanField(default=False)
  is_profile = models.BooleanField(default=False)
  
  class Meta:
    db_table = 'user'
  
  USERNAME_FIELD = 'email'
  EMAIL_FIELDS = 'email'
  
  objects = CustomUserManager()
  
  def __str__(self):
    return f'email:{self.email}'
  
  
class Buyer(models.Model):
  user = models.OneToOneField(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE,
                              primary_key=True)
  first_name = models.CharField(max_length=50)
  last_name = models.CharField(max_length=50)
  date_of_birth = models.DateField()
  phone = models.CharField(default='111-1111-1111', max_length=20)
  address = models.CharField(default='A県B市C町１−１−１',max_length=200)
  date_joined = models.DateTimeField(auto_now_add=True)
  payment_id = models.CharField(null=True, max_length=50)
  
  class Meta:
    db_table = 'buyer'

  def __str__(self):
    return f'email:{self.user.email} \
      full_name:{self.last_name} {self.first_name}'
  
  def get_absolute_url(self):
    return reverse('accounts:buyer_detail', 
                   kwargs={'pk': self.pk})


class Seller(models.Model):
  user = models.OneToOneField(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE,
                              primary_key=True)
  first_name = models.CharField(max_length=50)
  last_name = models.CharField(max_length=50)
  date_of_birth = models.DateField()
  phone = models.CharField(default='222-2222-2222', max_length=20)
  address = models.CharField(default='A県B市C町２−２−２', max_length=200)
  date_joined = models.DateTimeField(auto_now_add=True)
  farm_name = models.CharField(max_length=100)
  description = models.TextField('farm description', blank=True)
  image = models.ImageField(blank=True, null=True)
  
  class Meta:
    db_table = 'seller'

  def __str__(self):
    return f'email:{self.user.email} \
      full_name:{self.last_name} {self.first_name}'
  
  def get_absolute_url(self):
    return reverse('accounts:seller_detail', 
                   kwargs={'pk': self.pk})