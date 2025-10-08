from django.contrib import admin, messages
from django.contrib.auth.models import User,Group
from .models import kobanya150_Idoszak, kobanya150_Alkalom

admin.site.register(kobanya150_Idoszak)

class kobanya150_AlkalomAdmin(admin.ModelAdmin):
    filter_horizontal = ('jelentkezok',)
    list_per_page = 200
    actions = ['add_jelentkezok_to_group', 'delete_selected_users']

    @admin.action(description="addd group")
    def add_jelentkezok_to_group(self, request, queryset):
        group, _ = Group.objects.get_or_create(name='kobanya150_jelentkezo')
        count = 0

        for alkalom in queryset:
            for user in alkalom.jelentkezok.all():
                if group not in user.groups.all():
                    user.groups.add(group)
                    count += 1

        self.message_user(request, f"{count} felhasználó hozzáadva a 'kobanya150_jelentkezo' csoporthoz.")

    add_jelentkezok_to_group.short_description = "Jelentkezők hozzáadása a kobanya150_jelentkezo csoporthoz"
    
    @admin.action(description="❌ Delete selected users from this Alkalom (and database)")
    def delete_selected_users(self, request, queryset):
        filter_horizontal = ('jelentkezok',)
        group = Group.objects.get(name="kobanya150_jelentkezo")
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
