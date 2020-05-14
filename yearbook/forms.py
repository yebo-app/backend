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
    """
    def save(self, commit=True):
        user = super().save(commit=False)

        user.first_name = self.cleaned_data('first_name')
        user.last_name = self.cleaned_data('last_name')
        user.email = self.cleaned_data('email')

        if commit:
            user.save()
        return user
    """

class YearbookUserRegistrationForm(forms.ModelForm):
    class Meta:
        model = YearbookUser
        fields = ['bio']

class SignatureForm(forms.ModelForm):
    class Meta:
        model = Signature
        fields = ['signature']

class YearbookUserUpdateForm(forms.ModelForm):
    class Meta:
        model = YearbookUser
        fields= ['bio']
