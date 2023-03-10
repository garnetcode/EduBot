"""Users Admin"""
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.conf import settings
from django.contrib import admin

# pylint: disable = no-name-in-module
from users.models import User


admin.site.site_header = f"{settings.PLATFORM_NAME} Super Admin"
admin.site.site_title = "Admin Portal"
admin.site.index_title = f"{settings.PLATFORM_NAME} Admin"


"""
    REGISTERING MODELS TO THE ADMIN PANEL
"""


@admin.register(User)
class UsersAdmin(BaseUserAdmin):
    """Users Admin"""
    #pylint: disable = no-member
    #pylint: disable = protected-access
    list_display = [i.name for i in User._meta.fields]
    list_filter = ('is_active', 'is_staff', 'is_superuser', 'role')
