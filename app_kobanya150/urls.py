from django.urls import path
from app_kobanya150.views import *

urlpatterns = [
    path('', index, name="kobanya150_index"),
    path('feljelentkezes/<int:id>/', feljelentkezes, name="feljelentkezes"),
    path('lejelentkezes/<int:id>/', lejelentkezes, name="lejelentkezes"),
    path('atjelentkezes/<int:id>/', atjelentkezes, name="atjelentkezes"),
    # path('error/', error_response, name="error_response"),
]
