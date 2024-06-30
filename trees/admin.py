from django.contrib import admin
from .models import Tree, PlantedTree


class PlantedTreeAdmin(admin.ModelAdmin):
    list_display = (
        "tree",
        "user",
        "age",
        "planted_at",
        "account",
        "latitude",
        "longitude",
    )
    search_fields = ("tree__name", "user__username", "account__name")
    list_filter = ("tree", "user", "account")


admin.site.register(Tree)
admin.site.register(PlantedTree, PlantedTreeAdmin)
