from django.urls import path
from app_kobanya150.views import *

urlpatterns = [
    path('', index, name="kobanya150_index"),
    # path('jelentkezes/<int:het_id>/', jelentkezes, name="jelentkezes"),
    # path('leiratkozas/<int:het_id>/', leiratkozas, name="leiratkozas"),
    # path('error/', error_response, name="error_response"),
]
