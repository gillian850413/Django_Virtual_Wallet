from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User, AbstractUser
from django.urls import reverse


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birthday = models.DateField(default=None)
    address = models.CharField(max_length=255, default=None)

    def __str__(self):
        return self.user.username


class Account(models.Model):
    account_id = models.AutoField(primary_key=True)
    balance = models.FloatField(default=0.00)
    user = models.ForeignKey(User, related_name='account_owner', on_delete=models.PROTECT)

    def __str__(self):
        return '%d' % self.balance

    def save(self, *args, **kwargs):
        # ensure that the database only stores 2 decimal places
        self.balance = round(self.balance, 2)
        super(Account, self).save(*args, **kwargs)


class Bank(models.Model):
    bank_id = models.AutoField(primary_key=True)
    owner_first_name = models.CharField(max_length=255, default=None)
    owner_last_name = models.CharField(max_length=255, default=None)
    routing_number = models.CharField(max_length=9, default=None)
    account_number = models.CharField(max_length=10, default=None)
    user = models.ForeignKey(User, related_name='bank_user', on_delete=models.PROTECT)

    def __str__(self):
        return '****%s' % self.account_number[:-4]

    def get_absolute_url(self):
        return reverse('bank_detail', kwargs={'pk': self.pk})

    def get_delete_url(self):
        return reverse('bank_delete', kwargs={'pk': self.pk})

    class Meta:
        unique_together = ('routing_number', 'account_number')


Card_Type = (
    ('credit', 'Credit Card'),
    ('debit', 'Debit Card'),
)


class Card(models.Model):
    card_id = models.AutoField(primary_key=True)
    card_type = models.CharField(max_length=45, choices=Card_Type)
    card_number = models.CharField(max_length=16, default=None)
    owner_first_name = models.CharField(max_length=45)
    owner_last_name = models.CharField(max_length=45)
    security_code = models.CharField(max_length=3, default=None)
    expiration_date = models.DateField(default=None)
    user = models.ForeignKey(User, related_name='card_user', on_delete=models.PROTECT)

    def get_absolute_url(self):
        return reverse('card_detail', kwargs={'pk': self.pk})

    def get_update_url(self):
        return reverse('card_update', kwargs={'pk': self.pk})

    def get_delete_url(self):
        return reverse('card_delete', kwargs={'pk': self.pk})

    def __str__(self):
        return '************%s' % (self.card_number[:-12])

    class Meta:
        unique_together = ('card_type', 'owner_first_name', 'owner_last_name', 'card_number', 'security_code', 'expiration_date')
        ordering = ['card_type', 'card_number']


Transaction_Type = (
    ('pay', 'Pay'),
    ('request', 'Request'),
    ('transfer', 'Transfer'),
)


Categories = (
    ('bank', 'Bank Transactions'),
    ('utilities', 'Bills & Utilities'),
    ('transportation', 'Auto & Transport'),
    ('groceries', 'Groceries'),
    ('shopping', 'Shopping'),
    ('health', 'Healthcare'),
    ('education', 'Education'),
    ('travel', 'Travel'),
    ('housing', 'Housing'),
    ('entertainment', 'Entertainment'),
    ('others', 'Others'),
)


Payment_Method = (
    ('account', 'Account'),
    ('credit', 'Credit Card'),
    ('debit', 'Debit Card'),
    ('bank', 'Bank'),
)


class Transaction(models.Model):
    transaction_id = models.AutoField(primary_key=True)
    transaction_type = models.CharField(max_length=45, choices=Transaction_Type, default='')
    category = models.CharField(max_length=45, choices=Categories)
    amount = models.FloatField(default=0.00)
    description = models.CharField(max_length=200)
    recipients = models.CharField(max_length=45)  # another user, friend, bank
    payment_method = models.CharField(max_length=45, choices=Payment_Method, default='Account')
    create_date = models.DateTimeField(default=now, editable=False)
    is_complete = models.BooleanField(default=False)
    account = models.ForeignKey(Account, related_name='accounts', on_delete=models.PROTECT, default=0.00)
    card = models.ForeignKey(Card, related_name='cards', on_delete=models.PROTECT)
    bank = models.ForeignKey(Bank, related_name='banks', on_delete=models.PROTECT)

    def save(self, *args, **kwargs):
        # ensure that the database only stores 2 decimal places
        self.amount = round(self.amount, 2)
        super(Transaction, self).save(*args, **kwargs)

    def __str__(self):
        return '%s %d (%s)' % (self.transaction_type, self.amount, self.category)

    class Meta:
        ordering = ['category']


class Friendship(models.Model):
    friendship_id = models.AutoField(primary_key=True)
    creator = models.ForeignKey(User, related_name="friendship_creator", on_delete=models.PROTECT)
    friend = models.ForeignKey(User, related_name="friend", on_delete=models.PROTECT)
