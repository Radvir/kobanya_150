from django.urls import path
from app_repont.views import index, jelentkezes, leiratkozas, error_response

urlpatterns = [
    path('', index, name="repont_index"),
    path('jelentkezes/<int:het_id>/', jelentkezes, name="jelentkezes"),
    path('leiratkozas/<int:het_id>/', leiratkozas, name="leiratkozas"),
    path('error/', error_response, name="error_response"),
]
