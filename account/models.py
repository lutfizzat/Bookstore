from __future__ import unicode_literals
from typing import Tuple
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db.models.fields import BooleanField, DateTimeField
from django.core.validators import MaxValueValidator, MinValueValidator 
from django.db.models.signals import post_save
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from django.conf import settings
from django.shortcuts import reverse
#from django.core.exceptions import ValidationError

class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, password=None,):
        if not email:
            raise ValueError("Users must have an email address")
        if not username:
            raise ValueError("Users must have an username")
        
        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password,):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

# specifying choices
USERTYPE_CHOICES = (
    ("Administrator", "Administrator"),
    ("Buyer", "Buyer"),
)    

class Account(AbstractUser):
    
    email                      = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username                   = models.CharField(max_length=30, unique=True)
    usertype                   = models.CharField(max_length=30, choices= USERTYPE_CHOICES, default='Administrator')
    date_of_birth              = models.DateField(verbose_name=_("Date of birth"), blank=True, null=True)
    address1                   = models.CharField(verbose_name=_("Address line 1"), max_length=1024, blank=True, null=True)
    address2                   = models.CharField(verbose_name=_("Address line 2"), max_length=1024, blank=True, null=True)
    zip_code                   = models.CharField(verbose_name=_("Postal Code"), max_length=12, blank=True, null=True)
    city                       = models.CharField(verbose_name=_("City"), max_length=1024, blank=True, null=True)
    country                    = CountryField(blank=True, null=True)
    date_joined                = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login                 = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin                   = models.BooleanField(default=False)
    is_active                  = models.BooleanField(default=True)
    is_staff                   = models.BooleanField(default=False)
    is_superuser               = models.BooleanField(default=False)
    # is_administrator           = models.BooleanField(default=False)
    #is_buyer                   = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = MyAccountManager()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True



#types of choices for book category
CATEGORY_CHOICES = (
    ("horror", "horror"),
    ("thriller", "thriller"),
    ("romance", "romance"),
    ("supernatural", "supernatural"),
    ("action","action"),
)

PAYMENT_CHOICES = (
    ('S', 'Stripe'),
    ('P', 'Paypal'),
)

class Item(models.Model):
    title = models.CharField(max_length=200, null=True, blank=False)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, blank=False, null=True)
    price = models.PositiveIntegerField(default=False, null=True, blank=False, validators=[MinValueValidator(1)])
    quantity = models.PositiveIntegerField(default=0, null=True, blank=False, validators=[MinValueValidator(1)] )
    digital = models.BooleanField(default=False, null=True, blank=False)
    image = models.ImageField(null=True, blank=True)
    description = models.TextField(default=False, null=True, blank=False)
    slug = models.SlugField()

    def __str__(self):
        return self.title

    def get_add_to_cart_url(self):
        return reverse('add_to_cart', kwargs={'slug':self.slug})

    def get_remove_from_cart_url(self):
        return reverse('remove_from_cart', kwargs={'slug':self.slug})

    def get_remove_single_from_cart_url(self):
        return reverse('remove_single_from_cart', kwargs={'slug':self.slug})


    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url



class OrderItem(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, blank=True, null=True)
    item = models.OneToOneField(Item, on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.IntegerField(default=1, null=True, blank=True)
    title = models.CharField(max_length=200, null=True, blank=False)
    is_ordered = models.BooleanField(default=False)
   
    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_final_price(self):
        return self.get_total_item_price()

    
class Order(models.Model):
    ref_code = models.CharField(max_length=15)
    user = models.ForeignKey(Account, on_delete=models.CASCADE, blank=True, null=True)
    items = models.ManyToManyField(OrderItem)
    address = models.ForeignKey("Address", on_delete=models.SET_NULL, blank=True, null=True)
    is_ordered = models.BooleanField(default=False)
    date_ordered = models.DateTimeField(auto_now=True)

    def get_cart_items(self):
        return self.items.all()
        

    def __str__(self):
        return '{0} - {1}'.format(self.user, self.ref_code)

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        return total

    # def shipping(self):
    #     shipping = True
    #     order_items = self.order_item.items.all()
    #     return shipping


class Address(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, blank=True, null=True)
    street_address = models.CharField(max_length=200, null=True, blank=False)
    apartment_address = models.CharField(max_length=200, null=True, blank=False)
    country = CountryField(multiple=False)
    zip = models.CharField(max_length=200)
    save_info = models.BooleanField(default=False)
    default = models.BooleanField(default=False)
    use_default = models.BooleanField(default=False)
    payment_choice = models.CharField(choices=PAYMENT_CHOICES, max_length=2)

    def __str__(self):
        return self.user.username




   
