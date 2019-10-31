from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .models import (
    User,
    Account,
    Bank,
    Card,
    Transaction,
    Friendship,
)


class Index(View):
    def get(self, request):
        return render(request, 'index.html')

