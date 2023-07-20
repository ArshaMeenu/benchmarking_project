from django.contrib.auth.models import (AbstractBaseUser, AbstractUser,
                                        PermissionsMixin, User)
from django.core.validators import RegexValidator
from django.db import models
from django.db.models import Manager
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager

# Custom user model  - reference :https://testdriven.io/blog/django-custom-user-model/#forms

# class UserType(models.Model):  # 3.separate class for roles and manytomanyfield in usermodel
#     CUSTOMER = 1
#     SELLER = 2
#     TYPE_CHOICES = (
#         (SELLER, 'Seller'),
#         (CUSTOMER, 'Customer')
#     )
#
#     id = models.PositiveSmallIntegerField(choices=TYPE_CHOICES,primary_key=True)
#
#     def __str__(self):
#         return self.get_id_display()
#

class CustomUser(AbstractBaseUser, PermissionsMixin):
    # username = None
    email = models.EmailField(_('email address'), unique=True)
    name = models.CharField(max_length=255)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    # For multiple user type -3 ways to use
    # case of no extra fields # 1. using bollen field
    # is_customer = models.BooleanField(default=True)
    # is_seller = models.BooleanField(default=False)

    # # 2.choice field with django multiselect field
    # type =(
    #     (1,'seller'),
    #     (2,'customer')
    # )
    # user_type = models.IntegerField(choices=type,default=1)

    # 3.separate class for roles and manytomanyfield in usermodel
    # user_type = models.ManyToManyField(UserType)

    # case of extra fields # 1. using bollen field and separate classes for different types with onetoone field
    # is_customer = models.BooleanField(default=True)
    # is_seller = models.BooleanField(default=False)
    # case of extra fields # 2.proxy model

    class Types(models.TextChoices):
        SELLER = "Seller", "SELLER"
        CUSTOMER = "Customer", "CUSTOMER"

    default_type = Types.CUSTOMER
    type = models.CharField(_('Type'), max_length=255, choices=Types.choices, default=default_type)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    # if not the code below then taking default value in User model not in proxy model
    def save(self, *args, **kwargs):
        if not self.id:
            self.type = self.default_type
        return super().save(*args, **kwargs)


class CustomerAdditional(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)


class SellerAdditional(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    gst = models.CharField(max_length=255)
    warehouse_location = models.CharField(max_length=1000)


# model manager for proxy model
class SellerManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=CustomUser.Types.SELLER)


class CustomerManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=CustomUser.Types.CUSTOMER)


# Proxy Models .They don't create a separate table
class Seller(CustomUser):
    default_type = CustomUser.Types.SELLER
    objects = SellerManager()

    class Meta:
        proxy = True

    def sell(self):
        print('i can sell')

    @property
    def showAdditional(self):
        return self.selleradditional


class Customer(CustomUser):
    default_type = CustomUser.Types.CUSTOMER
    objects = CustomerManager()

    class Meta:
        proxy = True

    def buy(self):
        print('i can buy')

    @property
    def showAdditional(self):
        return self.customeradditional


# class Customer(models.Model):
#     user = models.OneToOneField(CustomUser,on_delete=models.CASCADE)
#     address = models.CharField(max_length=255)
#
#
# class Seller(models.Model):
#     user = models.OneToOneField(CustomUser,on_delete=models.CASCADE)
#     gst = models.CharField(max_length=255)
#     warehouse_location = models.CharField(max_length=1000)


# class CustomUser(AbstractUser):
#     username = None
#     email = models.EmailField(_('email address'), unique=True)
#
#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = []
#
#     objects = CustomUserManager()
#
#     def __str__(self):
#         return self.email


# Customize Django Models using @classmethod decorator.
class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=255)
    price = models.FloatField()

    @classmethod
    def updateprice(cls, product_id, price):
        product = cls.objects.filter(product_id=product_id)
        product = product.first()
        product.price = price
        product.save()
        return product

    @classmethod
    def create(cls, product_name, price):
        product = Product(product_name=product_name, price=price)
        product.save()
        return product

    def __str__(self):
        return self.product_name


# Customize Django Models using models.Manager
class CartManager(models.Manager):
    def create_cart(self, user):
        cart = self.create(user=user)
        return cart

    def get_queryset(self):
        return super().get_queryset().all()


class Cart(models.Model):
    cart_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    created_on = models.DateTimeField(default=timezone.now)

    manager = Manager()
    carts = CartManager()


class ProductInCart(models.Model):
    class Meta:
        unique_together = (('cart', 'product'),)

    product_in_cart_id = models.AutoField(primary_key=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()


class Order(models.Model):
    status_choices = {
        (1, 'Not packed'),
        (2, 'ready for shipment'),
        (3, 'shipped'),
        (4, 'delivered')
    }
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    status = models.IntegerField(choices=status_choices, default=1)


class Deal(models.Model):
    user = models.ManyToManyField(CustomUser)
    deal_name = models.CharField(max_length=255)


class Contact(models.Model):
    email = models.EmailField()
    name = models.CharField(max_length=100)
    phone_regex = RegexValidator(regex=r'^\d{10}$', message="Phone number must consist of 10 digits")
    phone = models.CharField(max_length=255, validators=[phone_regex])
    query = models.TextField()
