from django.contrib import admin
from .models import Account


class AccountAdmin(admin.ModelAdmin):
    list_display = ("name", "created", "active", "created_by")
    list_filter = ("active",)
    search_fields = ("name",)
    filter_horizontal = ("users",)
    actions = ["activate_accounts", "deactivate_accounts"]

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

    def activate_accounts(self, request, queryset):
        queryset.update(active=True)

    activate_accounts.short_description = "Activate selected accounts"

    def deactivate_accounts(self, request, queryset):
        queryset.update(active=False)

    deactivate_accounts.short_description = "Deactivate selected accounts"


admin.site.register(Account, AccountAdmin)
