from django import forms
from django.db import transaction
# from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .models import User, Customer, Store

# from django.core.exceptions import ValidationError
# from phonenumber_field.formfields import PhoneNumberField
import uuid
import os


class RegisterCustomerForm(UserCreationForm):

    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)

    ''' There are two types of user, customer and store '''
    class Meta(UserCreationForm.Meta):
        model = User

        UserCreationForm.Meta.fields = ('email',)
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name')

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_customer = True
        user.save()
        customer = Customer.objects.create(user=user)
        customer.first_name = self.cleaned_data.get('first_name')
        customer.last_name = self.cleaned_data.get('last_name')
        customer.email = self.cleaned_data.get('email')
        customer.save()

        return customer


class RegisterStoreForm(UserCreationForm):
    email = forms.EmailField(required=True)
    store_name = forms.CharField(required=True)
    company_name = forms.CharField(required=True)
    logo = forms.ImageField(required=False)
    address = forms.CharField(required=True)
    # identifier = forms.CharField(required=True)

    ''' There are two types of user, customer and store '''
    class Meta(UserCreationForm.Meta):
        model = User

        UserCreationForm.Meta.fields = ('email',)
        fields = UserCreationForm.Meta.fields + \
            ('store_name', 'company_name', 'logo', 'address')

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_store = True
        user.save()
        # Store creation
        store = Store.objects.create(user=user)
        store.identifier = uuid.uuid4().hex[:20]
        store.store_name = self.cleaned_data.get('store_name')
        store.company_name = self.cleaned_data.get('company_name')
        store.logo = self.cleaned_data.get('logo')
        store.address = self.cleaned_data.get('address')
        store.email = self.cleaned_data.get('email')

        store.save()

        def content_file_name(instance, filename):
            store.logo = filename.split('.')[-1]
            filename = "%s.%s" % (store.identifier, ext)
            return os.path.join('uploads', filename)

        return user
# ==============================================================
# class RegisterForm(UserCreationForm):

#     username = forms.CharField()
#     email = forms.EmailField()
#     first_name = forms.CharField(max_length=30)
#     last_name = forms.CharField(max_length=30)

#     # middleName = forms.CharField(required=False, max_length=20)
#     # lastName = forms.CharField(max_length=20)

#     class Meta:
#         model = User
#         fields = ["username", "first_name", "last_name",
#                   "email", "password1", "password2"]

#     def clean(self):
#         email = self.cleaned_data.get('email')
#         username = self.cleaned_data.get('username')
#         first_name = self.cleaned_data.get('first_name')
#         last_name = self.cleaned_data.get('last_name')

#         if User.objects.filter(email=email).exists():
#             raise ValidationError(
#                 "Ese correo ya está registrado en el sistema")
#         if User.objects.filter(username=username).exists():
#             raise ValidationError(
#                 "Ese nombre de usuario ya existe")

#         return self.cleaned_data


# class RegisterStoreForm(UserCreationForm):

#     # username = forms.CharField()
#     email = forms.EmailField()
#     store_name = forms.CharField(required=True)
#     company_name = forms.CharField(required=True)
#     address = forms.CharField(required=True)
#     logo = forms.ImageField(required=False)

#     class Meta:
#         model = User
#         fields = ["store_name", "company_name",
#                   "email", "address", "logo", "password1", "password2"]

#     def clean(self):
#         email = self.cleaned_data.get('email')
#         store_name = self.cleaned_data.get('store_name')
#         company_name = self.cleaned_data.get('company_name')
#         # username = self.cleaned_data.get('username')
#         address = self.cleaned_data.get('address')

#         if User.objects.filter(email=email).exists():
#             raise ValidationError(
#                 "Ese correo ya está registrado en el sistema")
#         # if User.objects.filter(username=username).exists():
#         #     raise ValidationError(
#         #         "Ese nombre de usuario ya existe")
#         if (User.objects.filter(company_name=company_name).exists() and User.objects.filter(store_name=store_name).exists()):
#             raise ValidationError(
#                 "El nombre de la compañia y el nombre de la tienda ya han sido registrados.")

#         return self.cleaned_data
