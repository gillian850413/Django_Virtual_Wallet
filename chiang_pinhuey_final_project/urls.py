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
    StaffLogin,
    StaffLogout
)

urlpatterns = [
    path('',
         RedirectView.as_view(
             pattern_name='index',
             permanent=False
         )),

    path('admin/', admin.site.urls),

    path('user/login/', UserLogin.as_view(template_name='app/login.html'), name='user_login'),
    path('user/logout/', UserLogout.as_view(), name='user_logout'),
    path('user/registration/', UserRegistration.as_view(), name='registration'),
    path('user/reset-password/', UserResetPwd.as_view(), name='reset_password'),

    path('staff/login/', StaffLogin.as_view(template_name='staff/staff_login.html'), name='staff_login'),
    path('staff/logout/', StaffLogout.as_view(), name='staff_logout'),

    path('', include('app.urls'))



] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
