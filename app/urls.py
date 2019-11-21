from django.contrib import admin
from django.urls import path, include
from app.views import (
    Index, StaffIndex, UserProfile, UserProfileUpdate, Activity,
    Send, Request, Friends, Wallet, Payment,
    BankCardInfo, BankCreate, BankDetail, BankDelete,
    CardCreate, CardDetail, CardUpdate, CardDelete)

urlpatterns = [
    path('index/', Index.as_view(), name='index'),
    path('settings/user-profile/', UserProfile.as_view(), name='profile'),
    path('settings/user-profile/edit/', UserProfileUpdate.as_view(), name='profile_update'),
    path('settings/bank-card-info/', BankCardInfo.as_view(), name='bank_card'),
    path('settings/bank/add/', BankCreate.as_view(), name='bank_create'),
    path('settings/bank/<int:pk>/detail/', BankDetail.as_view(), name='bank_detail'),
    path('settings/bank/<int:pk>/delete/', BankDelete.as_view(), name='bank_delete'),

    path('settings/card/add/', CardCreate.as_view(), name='card_create'),
    path('settings/card/<int:pk>/detail/', CardDetail.as_view(), name='card_detail'),
    path('settings/card/<int:pk>/update/', CardUpdate.as_view(), name='card_update'),
    path('settings/card/<int:pk>/delete/', CardDelete.as_view(), name='card_delete'),

    path('settings/payment-method/', Payment.as_view(), name='payment'),

    path('activity/', Activity.as_view(), name='activity'),
    path('transfer/send/', Send.as_view(), name='send'),
    path('transfer/request/', Request.as_view(), name='request'),
    path('transfer/friends/', Friends.as_view(), name='friends'),
    path('wallet/', Wallet.as_view(), name='wallet'),

    path('staff/', StaffIndex.as_view(), name='staff_index'),
]
