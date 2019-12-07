from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static

from app.views import (
    UserLogin,
    UserLogout,
    UserRegistration,
    UserResetPwd,
)

urlpatterns = [
    path('',
         RedirectView.as_view(
             pattern_name='index',
             permanent=False
         )),

    path('admin/', admin.site.urls),

    path('login/', UserLogin.as_view(template_name='app/login.html'), name='user_login'),
    path('logout/', UserLogout.as_view(), name='user_logout'),
    path('registration/', UserRegistration.as_view(), name='registration'),
    path('reset-password/', UserResetPwd.as_view(), name='reset_password'),

    path('', include('app.urls'))



] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
