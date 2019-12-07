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


Method_Type = (
    ('account', 'Easy Pay Account'),
    ('card', 'Cards'),
    ('bank', 'Bank'),
)


class PaymentMethod(models.Model):
    method_id = models.AutoField(primary_key=True)
    method_type = models.CharField(max_length=255, default=None, choices=Method_Type)
    user = models.ForeignKey(User, related_name='payment_user', on_delete=models.PROTECT)


class Account(PaymentMethod):
    balance = models.FloatField(default=0.00)

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse('wallet', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        # ensure that the database only stores 2 decimal places
        self.balance = round(self.balance, 2)
        super(Account, self).save(*args, **kwargs)


class Bank(PaymentMethod):
    owner_first_name = models.CharField(max_length=255, default=None)
    owner_last_name = models.CharField(max_length=255, default=None)
    routing_number = models.CharField(max_length=9, default=None)
    account_number = models.CharField(max_length=10, default=None)

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


class Card(PaymentMethod):
    card_type = models.CharField(max_length=45, choices=Card_Type)
    card_number = models.CharField(max_length=16, default=None)
    owner_first_name = models.CharField(max_length=45)
    owner_last_name = models.CharField(max_length=45)
    security_code = models.CharField(max_length=3, default=None)
    expiration_date = models.DateField(default=None)

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
    ('bank', 'Bank Transfer'),
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


class Transaction(models.Model):
    transaction_id = models.AutoField(primary_key=True)
    transaction_type = models.CharField(max_length=45, choices=Transaction_Type, default='')
    category = models.CharField(max_length=45, choices=Categories)
    amount = models.FloatField(default=0.00)
    description = models.CharField(max_length=200)
    recipients = models.CharField(max_length=45)  # another user, friend, bank
    create_date = models.DateTimeField(default=now, editable=False)
    is_complete = models.BooleanField(default=False)
    user = models.ForeignKey(User, related_name='tran_user', on_delete=models.PROTECT)
    payment_method = models.ForeignKey(PaymentMethod, related_name='payment_method', on_delete=models.PROTECT, default='')

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
