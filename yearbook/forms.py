from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.db import models
from django.forms import modelformset_factory

from .models import *

class UserLoginForm(forms.ModelForm):
    class Meta:
        model = YearbookUser
        fields = ['user']

class UserRegistrationForm(UserCreationForm):
    def clean_email(self):
        if User.objects.filter(email=self.cleaned_data['email']).exists():
            raise forms.ValidationError("The given email is already registered.")
        return self.cleaned_data['email']

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

class YearbookUserRegistrationForm(forms.ModelForm):
    class Meta:
        model = YearbookUser
        fields = ['bio']

class SignatureForm(forms.ModelForm):
    class Meta:
        model = Signature
        fields = ['signature']
        widgets = {
            'signature': forms.Textarea(
                attrs = {
                    'class' : "form-control",
                    'id' : "label-textarea2",
                    'rows' : "3",
                    'placeholder' : "Sign Here"
                }
            ),
        }

class SignatureDeleteForm(forms.ModelForm):
    class Meta:
        model = Signature
        fields = []

class YearbookUserUpdateForm(forms.ModelForm):
    avatar = forms.ImageField()

    class Meta:
        model = YearbookUser
        fields = ['bio', 'avatar']
        widgets = {
            'bio': forms.TextInput(
                attrs = {
                    'class' : "form-control",
                }
            ),
            'avatar': forms.FileInput(
                attrs = {
                }
            )
        }

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']
        widgets = {
            'username': forms.TextInput(
                attrs = {
                    'class' : "form-control",
                }
            ),
            'first_name': forms.TextInput(
                attrs = {
                    'class' : "form-control",
                }
            ),
            'last_name': forms.TextInput(
                attrs = {
                    'class' : "form-control",
                }
            ),
        }

class UserDeleteForm(forms.ModelForm):
    class Meta:
        model = User
        fields = []

class IYPUpdateForm(forms.ModelForm):
    class Meta:
        model = InstitutionYearProfile
        fields = ['yearbook_quote', 'yearbook_picture']

class SignatureUpdateForm(forms.ModelForm):
    signature = forms.CharField(required=False)

    class Meta:
        model = Signature
        fields = ['signature']
        widgets = {
            'signature': forms.Textarea
                (attrs = {
                    'class' : "form-control",
                    'id' : "label-textarea2",
                    'rows' : "3",
                    'placeholder' : "Update Signature Here"
                }
            ),
        }

class InstitutionCreationForm(forms.ModelForm):
    class Meta:
        model = Institution
        fields  = ['institution_name', 'institution_city', 'institution_state', 'institution_year_founded', 'logo']

class InstitutionYearProfileCreationForm(forms.Form):
    institution = forms.ModelChoiceField(Institution.objects.filter(approved=True))
    start_year = forms.IntegerField()
    end_year = forms.IntegerField()

class IYPDeleteForm(forms.ModelForm):
    class Meta:
        model = InstitutionYearProfile
        fields = []

class InstitutionJoinForm(forms.Form):
    institutionyears = forms.ModelMultipleChoiceField(queryset=InstitutionYear.objects.all())

class InviteFriendForm(forms.Form):
    friend_email = forms.EmailField()

class SingleYearInstitutionJoinForm(forms.ModelForm):
    class Meta:
        model = InstitutionYearProfile
        fields = []
