from django.contrib import admin
from django.urls import path, include
from app.views import (
    Index, UserProfile, UserProfileUpdate, ActivityList,
    SendSearchUser, SendDetail, RequestSearchUser, RequestDetail, Friends, WalletList,
    BankCreate, BankDetail, BankDelete,
    CardCreate, CardDetail, CardUpdate, CardDelete)

urlpatterns = [
    path('index/', Index.as_view(), name='index'),
    path('profile/', UserProfile.as_view(), name='profile'),
    path('profile/edit/', UserProfileUpdate.as_view(), name='profile_update'),

    path('wallet/', WalletList.as_view(), name='wallet'),
    path('bank/add/', BankCreate.as_view(), name='bank_create'),
    path('bank/<int:pk>/detail/', BankDetail.as_view(), name='bank_detail'),
    path('bank/<int:pk>/delete/', BankDelete.as_view(), name='bank_delete'),

    path('card/add/', CardCreate.as_view(), name='card_create'),
    path('card/<int:pk>/detail/', CardDetail.as_view(), name='card_detail'),
    path('card/<int:pk>/update/', CardUpdate.as_view(), name='card_update'),
    path('card/<int:pk>/delete/', CardDelete.as_view(), name='card_delete'),

    path('activity/', ActivityList.as_view(), name='activity'),
    path('send/', SendSearchUser.as_view(), name='send'),
    path('send/<int:pk>/', SendDetail.as_view(), name='send_detail'),

    path('request/', RequestSearchUser.as_view(), name='request'),
    path('request/<int:pk>/', RequestDetail.as_view(), name='request_detail'),

    path('friends/', Friends.as_view(), name='friends'),


]
