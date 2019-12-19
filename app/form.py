from django import forms
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.forms import TextInput
from datetime import date
from django.urls import reverse_lazy

from django.utils.html import format_html

from .models import (
    Profile,
    Bank,
    Card,
    Transaction
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
        if self.cleaned_data['birthday'] > date.today():
            self.add_error('birthday', 'Please input a valid birthday.')
        else:
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


class UserResetPwdForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('password', )

    def clean(self):
        cleaned_data = super(UserResetPwdForm, self).clean()
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password != confirm_password:
            self.add_error('confirm_password', 'Password and confirm password does not match.')

        return cleaned_data


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

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


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'

    def clean_birthday(self):
        return self.cleaned_data['birthday']

    def clean_address(self):
        return self.cleaned_data['address'].strip()


class BankCreateForm(forms.ModelForm):
    validator = RegexValidator(r"[0-9]", "Please input a valid bank account.")

    routing_number = forms.CharField(widget=TextInput(attrs={'type': 'number'}), validators=[validator])
    account_number = forms.CharField(widget=TextInput(attrs={'type': 'number'}), validators=[validator])

    class Meta:
        model = Bank
        exclude = ['user', 'method_type', 'payment']
        fields = '__all__'

    def clean_routing_number(self):
        if len(self.cleaned_data['routing_number']) != 9:
            self.add_error('routing_number', 'Routing number must be 9 digits')
        elif self.cleaned_data['routing_number'] == '':
            self.add_error('routing_number', 'The field "Routing number" is required.')
        else:
            return self.cleaned_data['routing_number'].strip()

    def clean_account_number(self):
        if len(self.cleaned_data['account_number']) != 10:
            self.add_error('account_number', 'Account number must be 10 digits')
        elif self.cleaned_data['account_number'] == '':
            self.add_error('account_number', 'The field "Account number" is required.')
        else:
            return self.cleaned_data['account_number'].strip()

    def clean_owner_first_name(self):
        if self.cleaned_data['owner_first_name'] == '':
            self.add_error('owner_first_name', 'The field "Account Holder First Name" is required.')
        else:
            return self.cleaned_data['owner_first_name'].strip()

    def clean_owner_last_name(self):
        if self.cleaned_data['owner_last_name'] == '':
            self.add_error('owner_last_name', 'The field "Account Holder Last Name" is required.')
        else:
            return self.cleaned_data['owner_last_name'].strip()


class CardCreateForm(forms.ModelForm):
    validator = RegexValidator(r"[0-9]", "Please input a valid card information.")
    card_number = forms.CharField(widget=TextInput(attrs={'type': 'number'}), validators=[validator])
    security_code = forms.CharField(widget=TextInput(attrs={'type': 'number'}), validators=[validator])

    FILTER_CHOICES = (
        ('Credit', 'Credit Card'),
        ('Debit', 'Debit Card'),
    )

    card_type = forms.ChoiceField(choices=FILTER_CHOICES)

    class Meta:
        model = Card
        exclude = ['user', 'method_type', 'payment']
        fields = '__all__'

    def clean_card_type(self):
        if self.cleaned_data['card_type'] == '':
            self.add_error('card_type', 'The field "Card Type" is required.')
        else:
            return self.cleaned_data.get('card_type')

    def clean_card_number(self):
        if len(self.cleaned_data['card_number']) != 16:
            self.add_error('card_number', 'Card number must be 16 digits')
        else:
            return self.cleaned_data['card_number'].strip()

    def clean_owner_first_name(self):
        if self.cleaned_data['owner_first_name'] == '':
            self.add_error('owner_first_name', 'The field "Card Holder First Name" is required.')
        else:
            return self.cleaned_data['owner_first_name'].strip()

    def clean_owner_last_name(self):
        if self.cleaned_data['owner_last_name'] == '':
            self.add_error('owner_last_name', 'The field "Card Holder Last Name" is required.')
        else:
            return self.cleaned_data['owner_last_name'].strip()

    def clean_security_code(self):
        if len(self.cleaned_data['security_code']) != 3:
            self.add_error('security_code', 'Security code must be 3 digits.')
        else:
            return self.cleaned_data['security_code'].strip()

    def clean_expiration_date(self):
        if self.cleaned_data['expiration_date'] < date.today():
            self.add_error('birthday', 'Please input a valid card.')
        else:
            return self.cleaned_data['expiration_date']


class BankUpdateForm(forms.ModelForm):
    class Meta:
        model = Bank
        exclude = ['user']
        fields = ('owner_first_name', 'owner_last_name')

    def clean_owner_first_name(self):
        return self.cleaned_data['owner_first_name'].strip()

    def clean_owner_last_name(self):
        return self.cleaned_data['owner_last_name'].strip()

    def __init__(self, *args, **kwargs):
        super(BankUpdateForm, self).__init__(*args, **kwargs)
        self.fields['owner_first_name'].error_messages = {'required': 'The field "Bank Holder First Name" is required'}
        self.fields['owner_last_name'].error_messages = {'required': 'The field "Bank Holder Last Name" is required'}


class CardUpdateForm(forms.ModelForm):
    class Meta:
        model = Card
        exclude = ['user']
        fields = ('owner_first_name', 'owner_last_name', 'expiration_date')

    def clean_owner_first_name(self):
        return self.cleaned_data['owner_first_name'].strip()

    def clean_owner_last_name(self):
        return self.cleaned_data['owner_last_name'].strip()

    def clean_expiration_date(self):
        return self.cleaned_data['expiration_date']

    def __init__(self, *args, **kwargs):
        super(CardUpdateForm, self).__init__(*args, **kwargs)
        self.fields['owner_first_name'].error_messages = {'required': 'The field "Card Holder First Name" is required'}
        self.fields['owner_last_name'].error_messages = {'required': 'The field "Card Holder Last Name" is required'}
        self.fields['expiration_date'].error_messages = {'required': 'Please input a valid card.'}


# check if the target user exist or not
class SearchUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username',)

    def clean_username(self):
        username = self.cleaned_data['username'].strip()
        return username


class SendMoneyForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ('category', 'amount', 'payment_method', 'description')

    def clean_category(self):
        return self.cleaned_data['category'].strip()

    def clean_amount(self):
        if self.cleaned_data['amount'] == 0:
            self.add_error('amount', 'The field "Amount" should not be 0.')
        else:
            return self.cleaned_data['amount']

    def clean_payment_method(self):
        payment = self.cleaned_data['payment_method']
        if payment.method_type == 'account' and payment.account.balance <= 0:
            message = format_html('Insufficient balance. <br> Please select another payment method or '
                                  'add a bank or card in <a href="{}">Wallet</a>.',
                                  reverse_lazy('account'))
            self.add_error('payment_method', message)
        else:
            return payment

    def clean_description(self):
        return self.cleaned_data['description']

    def __init__(self, *args, **kwargs):
        super(SendMoneyForm, self).__init__(*args, **kwargs)
        self.fields['category'].error_messages = {'required': 'The field "Category" is required'}
        self.fields['amount'].error_messages = {'required': 'The field "Amount" is required'}
        self.fields['payment_method'].error_messages = {'required': 'The field "Payment Method" is required'}
        self.fields['description'].error_messages = {'required': 'The field "Description" is required'}


class RequestMoneyForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ('category', 'amount', 'description')

    def clean_category(self):
        return self.cleaned_data['category'].strip()

    def clean_amount(self):
        if self.cleaned_data['amount'] == 0:
            self.add_error('amount', 'The field "Amount" should not be 0.')
        else:
            return self.cleaned_data['amount']

    def clean_description(self):
        return self.cleaned_data['description']

    def __init__(self, *args, **kwargs):
        super(RequestMoneyForm, self).__init__(*args, **kwargs)
        self.fields['category'].error_messages = {'required': 'The field "Category" is required'}
        self.fields['amount'].error_messages = {'required': 'The field "Amount" is required'}
        self.fields['description'].error_messages = {'required': 'The field "Description" is required'}


class CompletePaymentForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ('payment_method', )

    def clean_payment_method(self):
        payment = self.cleaned_data['payment_method']
        if payment.method_type == 'account' and payment.account.balance <= 0:
            message = format_html('Account balance is 0. <br> Please select another payment method or '
                                  'add a bank or card in <a href="{}">Wallet</a>.',
                                  reverse_lazy('account'))
            self.add_error('payment_method', message)
        else:
            return payment

    def __init__(self, *args, **kwargs):
        super(CompletePaymentForm, self).__init__(*args, **kwargs)
        self.fields['payment_method'].error_messages = {'required': 'The field "Payment Method" is required'}
