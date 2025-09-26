from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(kobanya150_Idoszak)

class kobanya150_AlkalomAdmin(admin.ModelAdmin):
    filter_horizontal = ('jelentkezok',)

admin.site.register(kobanya150_Alkalom, kobanya150_AlkalomAdmin)