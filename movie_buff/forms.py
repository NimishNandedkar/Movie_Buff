from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import *



class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['username', 'email','first_name', 'last_name',]



class ProfileUpdateForm(forms.ModelForm):
    birth_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False  #  field to be optional
    )
    class Meta:
        model = UserProfile
        fields = ['birth_date','gender','phone_number','profile_picture']        


class ChangePasswordForm(forms.Form):
    current_password = forms.CharField(
        label='Current Password',
        widget=forms.PasswordInput,
    )
    new_password = forms.CharField(
        label='New Password',
        widget=forms.PasswordInput,
    )
    confirm_password = forms.CharField(
        label='Confirm New Password',
        widget=forms.PasswordInput,
    )        