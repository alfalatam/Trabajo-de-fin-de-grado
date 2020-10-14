from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from usuarios.models import UserManager


# ==================== Standard User =============================

class User(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(unique=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    last_login = models.DateTimeField(auto_now_add=True)
    created = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = ('user')
        verbose_name_plural = ('users')
    is_store = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)
    # email = models.EmailField()

    # ==================== Customer ===============================


class Customer(models.Model):

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)


# ==================== Store ================================

class Store(models.Model):

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)

    store_name = models.CharField(max_length=100)

    identifier = models.CharField(max_length=20, default='')

    # company which owns the store (if have it)
    company_name = models.CharField(max_length=150)

    # To take the logo of the image
    logo = models.ImageField(blank=True, null=True)

    # Adress of the store
    address = models.CharField(max_length=150)
