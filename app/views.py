from symtable import Symbol

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView
from django.http import HttpResponseRedirect
from django.shortcuts import render, render_to_response, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib.auth.models import Group, User
from django.views import View
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, FormView

from app.form import (
    UserRegistrationForm,
    UserForm,
    UserProfileForm,
    UserResetPwdForm,
    BankCreateForm, CardCreateForm, CardUpdateForm)

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


class UserLogin(LoginView):
    def get_success_url(self):
        return reverse_lazy("index")


class UserLogout(LogoutView):
    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(reverse_lazy('user_login'))


class UserRegistration(CreateView):
    form_class = UserRegistrationForm
    model = User
    template_name = 'app/user_registration_form.html'

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):

        user = form.save()
        password = form.cleaned_data['password']

        user.set_password(password)
        user.save()

        group = Group.objects.get(name='normal_user')
        user.groups.add(group)

        # Create User Profile model
        Profile.objects.create(user=user, birthday=form.clean_birthday(), address=form.clean_address())

        # return super(UserRegistration, self).form_valid(form)
        return HttpResponseRedirect(reverse_lazy('user_login'))


class UserResetPwd(UpdateView):
    form_class = UserResetPwdForm
    model = User
    template_name = 'app/user_reset_pwd_form.html'
    success_url = 'user_login'

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.request.user

        password = form.cleaned_data['password']
        instance.user.set_password(password)
        instance.save()

        return HttpResponseRedirect(reverse_lazy('user_login'))


class UserProfile(LoginRequiredMixin, ListView):
    model = User
    template_name = 'app/user_profile_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nbar'] = 'profile'
        return context


class UserProfileUpdate(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserForm
    template_name = 'app/user_profile_update.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super(UserProfileUpdate, self).get_context_data(**kwargs)

        user = self.object
        profile = user.profile

        context['profile_form'] = UserProfileForm(instance=profile)
        context['nbar'] = 'profile'
        return context

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.request.user

        instance.save()

        user_profile, create= Profile.objects.update_or_create(user=instance.user)
        user_profile.birthday = self.request.POST['birthday']
        user_profile.address = self.request.POST['address']

        user_profile.save() #{form: 'profile_form'}

        return HttpResponseRedirect(reverse_lazy('profile'))


class BankCardInfo(LoginRequiredMixin, ListView):
    model = User
    template_name = 'app/bank_card_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['bank_list'] = Bank.objects.all()
        context['card_list'] = Card.objects.all()
        context['nbar'] = 'bank_card'
        return context


class BankCreate(LoginRequiredMixin, CreateView):
    form_class = BankCreateForm
    model = Bank
    template_name = 'app/bank_create.html'

    def get_context_data(self, **kwargs):
        context = super(BankCreate, self).get_context_data(**kwargs)
        context['user'] = self.request.user
        context['nbar'] = 'bank_card'
        return context

    def form_valid(self, form):
        bank = form.save(commit=False)
        bank.user = self.request.user

        bank.owner_first_name = form.cleaned_data['owner_first_name']
        bank.owner_last_name = form.cleaned_data['owner_first_name']
        bank.routing_number = form.cleaned_data['routing_number']
        bank.account_number = form.cleaned_data['account_number']

        bank.save()
        return HttpResponseRedirect(reverse_lazy('bank_card'))


class BankDetail(LoginRequiredMixin, View):
    def get(self, request, pk):
        bank = get_object_or_404(
            Bank,
            pk=pk
        )

        return render(
            request,
            'app/bank_detail.html',
            {'bank': bank, 'user': bank.user, 'nbar': 'bank_card'}
        )


class BankDelete(LoginRequiredMixin, DeleteView):
    model = Bank
    template_name = 'app/bank_confirm_delete.html'
    success_url = reverse_lazy('bank_card')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['nbar'] = 'bank_card'
        return context


class CardCreate(LoginRequiredMixin, CreateView):
    form_class = CardCreateForm
    model = Card
    template_name = 'app/card_create.html'

    def get_context_data(self, **kwargs):
        context = super(CardCreate, self).get_context_data(**kwargs)
        context['user'] = self.request.user
        context['nbar'] = 'bank_card'
        return context

    def form_valid(self, form):
        card = form.save(commit=False)
        card.user = self.request.user

        card.owner_first_name = form.cleaned_data['owner_first_name']
        card.owner_last_name = form.cleaned_data['owner_first_name']
        card.card_number = form.cleaned_data['card_number']
        card.card_type = form.cleaned_data['card_type']
        card.security_code = form.cleaned_data['security_code']
        card.expiration_date = form.cleaned_data['expiration_date']

        card.save()
        return HttpResponseRedirect(reverse_lazy('bank_card'))


class CardDetail(LoginRequiredMixin, View):
    def get(self, request, pk):
        card = get_object_or_404(
            Card,
            pk=pk
        )

        return render(
            request,
            'app/card_detail.html',
            {'card': card, 'user': card.user, 'nbar': 'bank_card'}
        )


class CardUpdate(LoginRequiredMixin, UpdateView):
    model = Card
    form_class = CardUpdateForm
    template_name = 'app/card_update.html'
    success_url = reverse_lazy('bank_card')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['nbar'] = 'bank_card'
        return context


class CardDelete(LoginRequiredMixin, DeleteView):
    model = Card
    template_name = 'app/card_confirm_delete.html'
    success_url = reverse_lazy('bank_card')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['nbar'] = 'bank_card'
        return context


class Payment(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'app/payment_setting.html', {'nbar': 'payment'})


class Send(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'app/transaction_send_form.html', {'nbar': 'send'})


class Request(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'app/transaction_request_form.html', {'nbar': 'request'})


class Friends(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'app/transaction_friends_form.html', {'nbar': 'friends'})


class Wallet(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'app/wallet_page.html')


class Activity(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'app/activity_page.html')


class StaffIndex(View):
    def get(self, request):
        return render(request, 'staff/staff_main_page.html')


class StaffLogin(LoginView):
    def get_success_url(self, request):
        return reverse_lazy("staff_index")


class StaffLogout(LogoutView):
    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(reverse_lazy('staff_login'))
