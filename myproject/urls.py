from django.contrib import admin
from django.urls import path, include
from app_regisztracio.views import valaszto, regisztracio

urlpatterns = [
    path('', valaszto),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('regisztracio/', regisztracio),
    path('repont/', include('app_repont.urls')),
    path('kobanya150/', include('app_kobanya150.urls')),
]
