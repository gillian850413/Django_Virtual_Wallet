from django.contrib import admin
from django.urls import path
from app.views import (
    Index,
)

urlpatterns = [
    path('index/', Index.as_view(), name='index'),

]