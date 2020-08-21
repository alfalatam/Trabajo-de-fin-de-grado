from django.db import models

# Create your models here.


# class Store(models.Model):
#     # Relaciones

#     # name of this store
#     name = models.CharField(max_length=50)

#     # company which owns the store (if have it)
#     company = models.CharField(max_length=50)

#     # To take the logo of the image
#     picture = models.ImageField()

#     # Adress of the store
#     address = models.CharField(max_length=50)

#     def __str__(self):
#         return "%s" % (self.name)

# from django.contrib.auth.models import AbstractUser
# from django.db import models


# class User(AbstractUser):
#     is_customer = models.BooleanField(default=False)
#     is_store = models.BooleanField(default=False)

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin


# class Store(AbstractBaseUser, PermissionsMixin):

#     email = models.EmailField(unique=True)

#     name = models.CharField(max_length=50)

#     # company which owns the store (if have it)
#     company = models.CharField(max_length=50)

#     # To take the logo of the image
#     picture = models.ImageField()

#     # Adress of the store
#     address = models.CharField(max_length=50)

#     objects = BaseUserManager()

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = []

#     class Meta:
#         verbose_name = ('user')
#         verbose_name_plural = ('users')

#     def __str__(self):
#         return "%s" % (self.name)
