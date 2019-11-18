from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.models import Group, User
from django.views import View
from django.views.generic import CreateView

from app.form import (
    UserRegistrationForm
)

from .models import (
    Profile,
    Account,
    Bank,
    Card,
    Transaction,
    Friendship,
)

from .utils import (
    ObjectCreateMixin,
)


class Index(View):
    def get(self, request):
        return render(request, 'index.html')


class UserRegistration(CreateView):
    form_class = UserRegistrationForm
    model = User
    template_name = 'app/user_registration_form.html'

    def form_valid(self, form):
        c = {'form': form, }

        user = form.save()
        password = form.cleaned_data['password']

        user.set_password(password)
        user.save()

        group = Group.objects.get(name='normal_user')
        user.groups.add(group)

        # Create User Profile model
        Profile.objects.create(user=user, birthday=form.clean_birthday(), address=form.clean_address())

        return super(UserRegistration, self).form_valid(form)

    def get_success_url(request):
        return reverse_lazy("user_login")


class UserLogin(LoginView):
    def get_success_url(self):
        return reverse_lazy("index")


class UserLogout(LogoutView):
    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(reverse_lazy('user_login'))


class UserResetPwd(View):
    def get(self, request):
        return render(request, 'app/user_reset_pwd_form.html')


class UserProfile(View):
    def get(self, request):
        return render(request, 'app/user_profile_form.html', {'nbar': 'profile'})


class BankCardInfo(View):
    def get(self, request):
        return render(request, 'app/bank_card_info.html', {'nbar': 'bank_card'})


class Payment(View):
    def get(self, request):
        return render(request, 'app/bank_card_payment_setting.html', {'nbar': 'payment'})


class Send(View):
    def get(self, request):
        return render(request, 'app/transaction_send_form.html', {'nbar': 'send'})


class Request(View):
    def get(self, request):
        return render(request, 'app/transaction_request_form.html', {'nbar': 'request'})


class Friends(View):
    def get(self, request):
        return render(request, 'app/transaction_friends_form.html', {'nbar': 'friends'})


class Wallet(View):
    def get(self, request):
        return render(request, 'app/wallet_page.html')


class Activity(View):
    def get(self, request):
        return render(request, 'app/activity_page.html')


class StaffIndex(View):
    def get(self, request):
        return render(request, 'staff/staff_main_page.html')


class StaffLogin(LoginView):
    def get_success_url(self):
        return reverse_lazy("staff_index")


class StaffLogout(LogoutView):
    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(reverse_lazy('staff_login'))
