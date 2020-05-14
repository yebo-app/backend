from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import *

class UserLoginForm(forms.ModelForm):
    class Meta:
        model = YearbookUser
        fields = ['user']

class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['first_name', 'last_name','username', 'email', 'password1', 'password2']

class YearbookUserRegistrationForm(UserRegistrationForm):
    class Meta:
        model = YearbookUser
        exclude = ['username', 'email', 'password']

class SignatureForm(forms.ModelForm):
    class Meta:
        model = Signature
        fields = ['signature']

class YearbookUserUpdateForm(forms.ModelForm):
    class Meta:
        model = YearbookUser
        fields= ['bio']