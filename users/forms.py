from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import *


# class SignUpForm(UserCreationForm):
#     class Meta:
#         model = User
#         fields = ('first_name', 'last_name', 'email','username', 'password1', 'password2', 'country', 'phone')

#     def save(self, commit=True):
#         user = super().save(commit=commit)
#         return user


# class UpdateProfileForm(UserChangeForm):
#     class Meta:
#         model = User
#         fields = ('username', 'email', 'first_name', 'last_name', 'country', 'phone')

#     # def save(self, commit=True):
#     #     user = super().save(commit=commit)
#     #     return user


# class ChangePasswordForm(forms.Form):
#     old_password = forms.CharField(widget=forms.PasswordInput())
#     new_password = forms.CharField(widget=forms.PasswordInput(),max_length=64)
#     new_password_repeated = forms.CharField(widget=forms.PasswordInput(),max_length=64)


# class DeleteUserForm(forms.Form):
#     password = forms.CharField(widget=forms.PasswordInput())