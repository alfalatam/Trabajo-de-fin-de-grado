from django import forms
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from phonenumber_field.formfields import PhoneNumberField


class RegisterForm(UserCreationForm):

    username = forms.CharField()
    email = forms.EmailField()
    # name = forms.CharField(max_length=20)
    # middleName = forms.CharField(required=False, max_length=20)
    # lastName = forms.CharField(max_length=20)

    class Meta:
        model = User
        fields = ["username",
                  #  "name", "middleName", "lastName",
                  "email", "password1", "password2"]

    def clean(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')

        if User.objects.filter(email=email).exists():
            raise ValidationError(
                "Ese correo ya está registrado en el sistema")
        if User.objects.filter(username=username).exists():
            raise ValidationError(
                "Ese nombre de usuario ya existe")

        return self.cleaned_data


# class UserProfileForm(forms.ModelForm):

#     class Meta:
#         model = UserProfile
#         fields = ('name', 'lastName', 'age')
