from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView
from django.http import HttpResponseRedirect
from django.shortcuts import render, render_to_response, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib.auth.models import Group, User
from django.db.models import Q, F
from django.views import View
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, FormView
from django.contrib import messages

from app.form import (
    UserRegistrationForm,
    UserForm,
    UserProfileForm,
    UserResetPwdForm,
    BankCreateForm,
    CardCreateForm,
    CardUpdateForm,
    SearchUserForm,
    SendMoneyForm,
    RequestMoneyForm,
    CompletePaymentForm,
)

from .models import (
    Profile,
    Account,
    Bank,
    Card,
    Transaction,
    PaymentMethod,
)

from .utils import (
    PageLinksMixin,
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
        payment = PaymentMethod.objects.create(user=user, method_type='account')
        Account.objects.create(payment=payment)

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
        return context

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.request.user
        instance.save()

        user_profile, create = Profile.objects.update_or_create(user=instance.user)
        user_profile.birthday = self.request.POST['birthday']
        user_profile.address = self.request.POST['address']

        user_profile.save()

        return HttpResponseRedirect(reverse_lazy('profile'))


class WalletList(LoginRequiredMixin, ListView):
    model = User
    template_name = 'app/wallet_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        context['bank_list'] = Bank.objects.filter(payment__user=user)
        context['card_list'] = Card.objects.filter(payment__user=user)
        context['account'] = Account.objects.filter(payment__user=user)
        return context


class AccountTransfer(LoginRequiredMixin, View):
    def get(self, request, pk):
        account = get_object_or_404(
            Account,
            pk=pk,
        )
        return render(request, 'app/account_transfer_confirm.html', {'account': account})

    def post(self, request, pk):
        Account.objects.filter(payment__method_id=self.kwargs.get('pk')).update(balance=0)
        return HttpResponseRedirect(reverse_lazy('wallet'))


class BankCreate(LoginRequiredMixin, CreateView):
    form_class = BankCreateForm
    model = Bank
    template_name = 'app/bank_create.html'

    def get_context_data(self, **kwargs):
        context = super(BankCreate, self).get_context_data(**kwargs)
        context['user'] = self.request.user
        return context

    def form_valid(self, form):
        bank = form.save(commit=False)
        bank.user = self.request.user
        bank.method_type = 'bank'
        bank.owner_first_name = form.cleaned_data['owner_first_name']
        bank.owner_last_name = form.cleaned_data['owner_first_name']
        bank.routing_number = form.cleaned_data['routing_number']
        bank.account_number = form.cleaned_data['account_number']

        payment = PaymentMethod.objects.create(user=bank.user, method_type=bank.method_type)
        Bank.objects.create(payment=payment,
                            owner_last_name=bank.owner_last_name,
                            owner_first_name=bank.owner_first_name,
                            routing_number=bank.routing_number,
                            account_number=bank.account_number)

        return HttpResponseRedirect(reverse_lazy('wallet'))


class BankDetail(LoginRequiredMixin, View):
    def get(self, request, pk):
        bank = get_object_or_404(
            Bank,
            pk=pk,
        )

        return render(
            request,
            'app/bank_detail.html',
            {'bank': bank, 'user': bank.payment.user}
        )


class BankDelete(LoginRequiredMixin, DeleteView):
    model = Bank
    template_name = 'app/bank_confirm_delete.html'
    # success_url = reverse_lazy('wallet')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def delete(self, request, *args, **kwargs):
        user = request.user

        bank = Bank.objects.get(id=kwargs.get('pk'))
        payment = PaymentMethod.objects.filter(user=user, method_id=bank.payment.method_id)
        bank.delete()
        payment.delete()

        return HttpResponseRedirect(reverse_lazy('wallet'))


class CardCreate(LoginRequiredMixin, CreateView):
    form_class = CardCreateForm
    model = Card
    template_name = 'app/card_create.html'

    def get_context_data(self, **kwargs):
        context = super(CardCreate, self).get_context_data(**kwargs)
        context['user'] = self.request.user
        return context

    def form_valid(self, form):
        card = form.save(commit=False)
        card.user = self.request.user
        card.method_type = 'card'
        card.owner_first_name = form.cleaned_data['owner_first_name']
        card.owner_last_name = form.cleaned_data['owner_first_name']
        card.card_number = form.cleaned_data['card_number']
        card.card_type = form.cleaned_data['card_type']
        card.security_code = form.cleaned_data['security_code']
        card.expiration_date = form.cleaned_data['expiration_date']

        payment = PaymentMethod.objects.create(user=card.user, method_type=card.method_type)
        Card.objects.create(payment=payment,
                            owner_last_name=card.owner_last_name,
                            owner_first_name=card.owner_first_name,
                            card_number=card.card_number,
                            card_type=card.card_type,
                            security_code=card.security_code,
                            expiration_date=card.expiration_date)

        return HttpResponseRedirect(reverse_lazy('wallet'))


class CardDetail(LoginRequiredMixin, View):
    def get(self, request, pk):
        card = get_object_or_404(
            Card,
            pk=pk
        )

        return render(
            request,
            'app/card_detail.html',
            {'card': card, 'user': card.payment.user}
        )


class CardUpdate(LoginRequiredMixin, UpdateView):
    model = Card
    form_class = CardUpdateForm
    template_name = 'app/card_update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_success_url(self):
        card_id = self.kwargs['pk']
        return reverse_lazy('card_detail', kwargs={'pk': card_id})


class CardDelete(LoginRequiredMixin, DeleteView):
    model = Card
    template_name = 'app/card_confirm_delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def delete(self, request, *args, **kwargs):
        user = request.user
        card = Card.objects.get(id=kwargs.get('pk'))
        payment = PaymentMethod.objects.filter(user=user, method_id=card.payment.method_id)
        card.delete()
        payment.delete()
        return HttpResponseRedirect(reverse_lazy('wallet'))


class ActivityList(LoginRequiredMixin, ListView, PageLinksMixin):
    paginate_by = 10
    model = Transaction
    template_name = 'app/activity_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        context['pay_list'] = Transaction.objects.filter(Q(creator=user, is_complete=True, transaction_type='send') |
                                                         Q(receiver=user, is_complete=True,
                                                           transaction_type='request')).order_by('-create_date')
        context['receive_list'] = Transaction.objects.filter(Q(receiver=user, is_complete=True, transaction_type='send') |
                                                            Q(creator=user, is_complete=True,
                                                            transaction_type='request')).order_by('-create_date')
        return context


class SendSearchUser(LoginRequiredMixin, ListView):
    model = User
    form_class = SearchUserForm
    template_name = 'app/send_search_user_form.html'

    def get_queryset(self):
        try:
            username = self.kwargs['search_user']
        except:
            username = ''

        if username != '':
            object_list = self.model.objects.filter(username=username)
        else:
            object_list = self.model.objects.all()
        return object_list

    def get_context_data(self, **kwargs):
        context = super(SendSearchUser, self).get_context_data(**kwargs)
        query = self.request.GET.get("search_user")
        context['user'] = self.request.user

        if query:
            queryset = (Q(username=query))
            search_user = User.objects.filter(queryset).distinct()
            if not search_user:
                messages.error(self.request, 'No user found.')
        else:
            search_user = []

        context['search_user'] = search_user
        context['nbar'] = 'send'

        return context


class SendMoney(LoginRequiredMixin, CreateView):
    form_class = SendMoneyForm
    model = Transaction
    template_name = 'app/send_money_form.html'

    def get_context_data(self, **kwargs):
        context = super(SendMoney, self).get_context_data(**kwargs)
        creator = self.request.user
        context['receiver'] = User.objects.get(id=self.kwargs.get('pk'))
        context['sender_payment_list'] = PaymentMethod.objects.filter(user=creator)
        context['nbar'] = 'send'
        return context

    def form_valid(self, form):
        transaction = form.save(commit=False)
        transaction.creator = self.request.user
        transaction.receiver = User.objects.get(id=self.kwargs.get('pk'))
        transaction.transaction_type = 'send'
        transaction.is_complete = True
        transaction.category = form.clean_category()
        transaction.amount = form.cleaned_data['amount']
        transaction.description = form.clean_description()
        transaction.payment_method = form.clean_payment_method()

        creator_payment = PaymentMethod.objects.filter(user=transaction.creator,
                                                       method_id=transaction.payment_method.method_id)
        creator_account = Account.objects.filter(payment=creator_payment[0])
        if creator_account:
            creator_account.update(balance=F('balance') - transaction.amount)

        receiver_payment = PaymentMethod.objects.filter(user=transaction.receiver, method_type='account')
        receiver_account = Account.objects.filter(payment=receiver_payment[0])
        receiver_account.update(balance=F('balance')+transaction.amount)

        transaction.save()
        return HttpResponseRedirect(reverse_lazy('send_success'))


class SendSuccess(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'app/send_success_page.html', {'nbar': 'send'})


class RequestSearchUser(LoginRequiredMixin, ListView):
    model = User
    form_class = SearchUserForm
    template_name = 'app/request_search_user_form.html'

    def get_queryset(self):
        try:
            username = self.kwargs['search_user']
        except:
            username = ''
        if username != '':
            object_list = self.model.objects.filter(username=username)
        else:
            object_list = self.model.objects.all()
        return object_list

    def get_context_data(self, **kwargs):
        context = super(RequestSearchUser, self).get_context_data(**kwargs)
        query = self.request.GET.get("search_user")
        context['user'] = self.request.user

        if query:
            queryset = (Q(username=query))
            search_user = User.objects.filter(queryset).distinct()
            if not search_user:
                messages.error(self.request, 'No user found.')
        else:
            search_user = []

        context['search_user'] = search_user
        context['nbar'] = 'request'

        return context


class RequestMoney(LoginRequiredMixin, CreateView):
    form_class = RequestMoneyForm
    model = Transaction
    template_name = 'app/request_money_form.html'

    def get_context_data(self, **kwargs):
        context = super(RequestMoney, self).get_context_data(**kwargs)
        creator = self.request.user
        context['receiver'] = User.objects.get(id=self.kwargs.get('pk'))
        context['request_payment_list'] = PaymentMethod.objects.filter(user=creator)
        context['nbar'] = 'request'
        return context

    def form_valid(self, form):
        transaction = form.save(commit=False)
        transaction.creator = self.request.user
        transaction.receiver = User.objects.get(id=self.kwargs.get('pk'))
        transaction.transaction_type = 'request'
        transaction.is_complete = False
        transaction.category = form.clean_category()
        transaction.amount = form.cleaned_data['amount']
        transaction.description = form.clean_description()
        transaction.save()

        return HttpResponseRedirect(reverse_lazy('request_success'))


class RequestSuccess(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'app/request_success_page.html', {'nbar': 'request'})


class IncompleteTranList(LoginRequiredMixin, ListView):
    model = Transaction
    template_name = 'app/transaction_incomplete_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['tran_creator_list'] = Transaction.objects.filter(creator=user, is_complete=False)
        context['tran_receiver_list'] = Transaction.objects.filter(receiver=user, is_complete=False)
        context['nbar'] = 'incomplete'
        return context


class IncompletePayment(LoginRequiredMixin, View):
    def get(self, request, pk):
        transaction = get_object_or_404(
            Transaction,
            pk=pk
        )

        return render(
            request,
            'app/transaction_incomplete_payment.html',
            {'tran': transaction, 'user': self.request.user, 'nbar': 'incomplete'}
        )


class IncompletePaymentConfirm(LoginRequiredMixin, UpdateView):
    model = Transaction
    form_class = CompletePaymentForm
    template_name = 'app/transaction_payment_confirm.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sender = self.request.user
        context['sender_list'] = PaymentMethod.objects.filter(user=sender)
        context['tran'] =  self.kwargs['pk']
        context['nbar'] = 'incomplete'
        return context

    def form_valid(self, form):
        transaction = form.save(commit=False)
        transaction.is_complete = True
        transaction.payment_method = form.clean_payment_method()

        sender = self.request.user
        sender_payment = PaymentMethod.objects.filter(user=sender, method_id=transaction.payment_method.method_id)
        sender_account = Account.objects.filter(payment=sender_payment[0])
        if sender_account:
            sender_account.update(balance=F('balance') - transaction.amount)

        # receiver is the person who create the request (transaction creator at this point)
        receiver_payment = PaymentMethod.objects.filter(user=transaction.creator, method_type='account')
        receiver_account = Account.objects.filter(payment=receiver_payment[0])
        receiver_account.update(balance=F('balance')+transaction.amount)

        transaction.save()
        return HttpResponseRedirect(reverse_lazy('payment_complete'))


class PaymentComplete(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'app/transaction_payment_success.html', {'nbar': 'incomplete'})


class IncompleteRequest(LoginRequiredMixin, View):
    def get(self, request, pk):
        transaction = get_object_or_404(
            Transaction,
            pk=pk
        )

        return render(
            request,
            'app/transaction_incomplete_request.html',
            {'tran': transaction, 'user': self.request.user, 'nbar': 'incomplete'}
        )


class IncompleteRequestDelete(LoginRequiredMixin, DeleteView):
    model = Transaction
    template_name = 'app/transaction_request_delete.html'
    success_url = reverse_lazy('incomplete')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tran'] = self.kwargs['pk']
        context['nbar'] = 'incomplete'
        return context
