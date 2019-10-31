from django.contrib import admin
from .models import User, Account, Bank, Card, Transaction, Friendship

admin.site.register(User)
admin.site.register(Account)
admin.site.register(Bank)
admin.site.register(Card)
admin.site.register(Transaction)
admin.site.register(Friendship)