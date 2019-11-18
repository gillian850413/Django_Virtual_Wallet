from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.shortcuts import redirect, render

from .models import (
    Profile,
    Account,
    Bank,
    Card,
    Transaction,
    Friendship,
)


class UserRegistrationForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    birthday = forms.DateField(required=False)
    address = forms.CharField(required=False)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password')

    def clean_username(self):
        return self.cleaned_data['username'].strip()

    def clean_first_name(self):
        if self.cleaned_data['first_name'] == '':
            self.add_error('first_name', 'The field "First Name" is required.')
        else:
            return self.cleaned_data['first_name'].strip()

    def clean_last_name(self):
        if self.cleaned_data['last_name'] == '':
            self.add_error('last_name', 'The field "Last Name" is required.')
        else:
            return self.cleaned_data['last_name'].strip()

    def clean_email(self):
        if self.cleaned_data['email'] == '':
            self.add_error('email', 'The field "Email" is required.')
        else:
            return self.cleaned_data['email'].strip()

    def clean_birthday(self):
        return self.cleaned_data['birthday']

    def clean_address(self):
        return self.cleaned_data['address'].strip()

    def clean(self):
        cleaned_data = super(UserRegistrationForm, self).clean()
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password != confirm_password:
            self.add_error('confirm_password', 'Password and confirm password does not match.')

        return cleaned_data

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['username'].error_messages = {'required': 'The field "Username" is required'}
        self.fields['password'].error_messages = {'required': 'The field "Password" is required'}
        self.fields['confirm_password'].error_messages = {'required': 'The field "Confirm Password" is required'}

        # for field in self.fields.values():
        #     field.error_messages = {'required':'The field "{fieldname}" is required'.format(
        #         fieldname=field.label)}


class UserResetPwdForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'password')

    def clean_email(self):
        return self.cleaned_data['email'].strip()

    def clean_password(self):
        return self.cleaned_data['password'].strip()

    def clean_confirm_password(self):
        return self.cleaned_data['confirm_password'].strip()
