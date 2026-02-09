# auth/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import UserProfile


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    fields = ('phone', 'whatsapp', 'profile_picture', 'bio', 'is_host')


class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_phone', 'is_host')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'profile__is_host')
    search_fields = ('username', 'first_name', 'last_name', 'email', 'profile__phone')

    def get_phone(self, obj):
        if hasattr(obj, 'profile'):
            return obj.profile.phone
        return ''
    get_phone.short_description = 'Phone'

    def is_host(self, obj):
        if hasattr(obj, 'profile'):
            return obj.profile.is_host
        return False
    is_host.boolean = True
    is_host.short_description = 'Host'


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'whatsapp', 'is_host', 'created_at')
    list_filter = ('is_host', 'created_at')
    search_fields = ('user__username', 'user__email', 'phone', 'whatsapp')
    raw_id_fields = ('user',)
    readonly_fields = ('created_at', 'updated_at')