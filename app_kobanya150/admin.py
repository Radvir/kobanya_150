from django.contrib import admin
from django.contrib.auth.models import Group
from .models import kobanya150_Idoszak, kobanya150_Alkalom

admin.site.register(kobanya150_Idoszak)

class kobanya150_AlkalomAdmin(admin.ModelAdmin):
    filter_horizontal = ('jelentkezok',)
    list_per_page = 200
    actions = ['add_jelentkezok_to_group']

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

admin.site.register(kobanya150_Alkalom, kobanya150_AlkalomAdmin)
