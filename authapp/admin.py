from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('roles',)}),
		('Hours', {'fields': ('hours_paid', 'hours_taken')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
