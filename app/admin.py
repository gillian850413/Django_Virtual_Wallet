from django.contrib import admin
from .models import Profile, Account, Bank, Card, Transaction, PaymentMethod

admin.site.register(Profile)
admin.site.register(Account)
admin.site.register(Bank)
admin.site.register(Card)
admin.site.register(Transaction)
admin.site.register(PaymentMethod)