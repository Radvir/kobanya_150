from django.contrib import admin, messages
from django.contrib.auth.models import User
from .models import *

# Register your models here.
admin.site.register(kobanya150_Idoszak)

class kobanya150_AlkalomAdmin(admin.ModelAdmin):
    filter_horizontal = ('jelentkezok',)
    
    actions = ['delete_selected_users']
    
    @admin.action(description="❌ Delete selected users from this Alkalom (and database)")
    def delete_selected_users(self, request, queryset):
        filter_horizontal = ('jelentkezok',)
        deleted_count = 0

        for alkalom in queryset:
            users_to_delete = alkalom.jelentkezok.filter(groups=group)
            deleted_count += users_to_delete.count()
            users_to_delete.delete()  # deletes User objects themselves

        self.message_user(
            request,
            f"Deleted {deleted_count} users from the database.",
            level=messages.WARNING
        )

admin.site.register(kobanya150_Alkalom, kobanya150_AlkalomAdmin)