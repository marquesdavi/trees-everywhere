# users/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from accounts.models import Account


class AccountInline(admin.TabularInline):
    model = Account.users.through
    extra = 1


class CustomUserAdmin(UserAdmin):
    inlines = [AccountInline]
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "is_active",
    )


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
