from django.contrib import admin
from django.urls import path, include
from .views import redirect_root_view
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', redirect_root_view),
    path('admin/', admin.site.urls),
    path('', include('app.urls'))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)