from django.db import models
from django.core.validators import MaxLengthValidator, MinLengthValidator
from django.utils.timezone import now


class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=45, unique=True)
    password = models.CharField(max_length=45, default='')

    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)

    class Meta:
        ordering = ['first_name', 'last_name']
        unique_together = (('first_name', 'last_name', 'email'),)


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
    routing_number = models.IntegerField(validators=[MinLengthValidator(9), MaxLengthValidator(9)])
    account_number = models.IntegerField(validators=[MinLengthValidator(10), MaxLengthValidator(12)])
    user = models.ForeignKey(User, related_name='bank_owner', on_delete=models.PROTECT)

    def __str__(self):
        return 'Bank ****%d' % self.account_number[:-4]

    class Meta:
        unique_together = ('routing_number', 'account_number')


Card_Type = (
    ('credit', 'Credit Card'),
    ('debit', 'Debit Card'),
)


class Card(models.Model):
    card_id = models.AutoField(primary_key=True)
    card_type = models.CharField(max_length=45, choices=Card_Type)
    card_number = models.IntegerField(validators=[MinLengthValidator(16), MaxLengthValidator(16)], unique=True)
    owner_first_name = models.CharField(max_length=45)
    owner_last_name = models.CharField(max_length=45)
    user = models.ForeignKey(User, related_name='card_owner', on_delete=models.PROTECT)

    def __str__(self):
        return '%s ****%d' % (self.card_type, self.card_number[:-4])

    class Meta:
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
