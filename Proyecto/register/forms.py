from django import forms
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django.core.exceptions import ValidationError
from phonenumber_field.formfields import PhoneNumberField


class RegisterForm(UserCreationForm):

    username = forms.CharField()
    email = forms.EmailField()
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)

    # middleName = forms.CharField(required=False, max_length=20)
    # lastName = forms.CharField(max_length=20)

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name",
                  #  "name", "middleName", "lastName",
                  "email", "password1", "password2"]

    def clean(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')

        if User.objects.filter(email=email).exists():
            raise ValidationError(
                "Ese correo ya está registrado en el sistema")
        if User.objects.filter(username=username).exists():
            raise ValidationError(
                "Ese nombre de usuario ya existe")

        return self.cleaned_data

    # def clean_username(self):
    #     username = self.cleaned_data.get('username')
    #     if User.objects.filter(username=username).exists():
    #         raise ValidationError(
    #             "Ese nombre de usuario ya existe")
    #     return self.cleaned_data

    # def clean_password(self):
    #     password1 = self.cleaned_data.get('password1')
    #     password2 = self.cleaned_data.get('password2')
    #     if not password1 == password2:
    #         raise ValidationError("Las contraseñas no coinciden")
    #     else:
    #         raise ValidationError(
    #             "Vaya, parece que ha habido algún problema con la contraseña,por favor vuelva a introducirla")
    #     return self.cleaned_data


class RegisterStoreForm(UserCreationForm):

    username = forms.CharField()
    email = forms.EmailField()
    store_name = forms.CharField(max_length=150)
    company_name = forms.CharField(max_length=150)
    address = forms.CharField(max_length=150)
    logo = forms.ImageField()

    class Meta:
        model = User
        fields = ["username", "store_name", "company_name",
                  "email", "address", "logo", "password1", "password2"]

    def clean(self):
        email = self.cleaned_data.get('email')
        store_name = self.cleaned_data.get('store_name')
        company_name = self.cleaned_data.get('company_name')
        username = self.cleaned_data.get('username')
        address = self.cleaned_data.get('address')

        if User.objects.filter(email=email).exists():
            raise ValidationError(
                "Ese correo ya está registrado en el sistema")
        if User.objects.filter(username=username).exists():
            raise ValidationError(
                "Ese nombre de usuario ya existe")
        if (User.objects.filter(company_name=company_name).exists() and User.objects.filter(store_name=store_name).exists()):
            raise ValidationError(
                "El nombre de la compañia y el nombre de la tienda ya han sido registrados.")

        return self.cleaned_data
