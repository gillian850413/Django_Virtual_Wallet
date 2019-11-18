from django.contrib import admin
from django.urls import path, include
from app.views import (
    Index,
    Activity,
    Send,
    Request,
    Friends,
    Wallet,
    UserResetPwd,
    UserRegistration,
    UserProfile,
    BankCardInfo,
    Payment,
    StaffIndex,
)

urlpatterns = [
    path('index/', Index.as_view(), name='index'),
    path('activity/', Activity.as_view(), name='activity'),
    path('transfer/send/', Send.as_view(), name='send'),
    path('transfer/request/', Request.as_view(), name='request'),
    path('transfer/friends/', Friends.as_view(), name='friends'),
    path('wallet/', Wallet.as_view(), name='wallet'),
    path('settings/user-profile/', UserProfile.as_view(), name='profile'),
    path('settings/bank-card-info/', BankCardInfo.as_view(), name='bank_card'),
    path('settings/payment-method/', Payment.as_view(), name='payment'),
    path('staff/', StaffIndex.as_view(), name='staff_index'),
]
