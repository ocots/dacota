from django.contrib import admin
from django.contrib.sessions.models import Session

from .models import BinaryRelation, Component

# Register your models here.


class ComponentAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "a", "b", "c")
    filter_horizontal = ("sessions",)


class BinaryRelationAdmin(admin.ModelAdmin):
    list_display = ("id", "component1", "component2", "a12", "a21", "alpha")
    filter_horizontal = ("sessions",)


class SessionAdmin(admin.ModelAdmin):
    def _session_data(self, obj):
        return obj.get_decoded()

    list_display = ["session_key", "_session_data", "expire_date"]


admin.site.register(Session, SessionAdmin)
admin.site.register(Component, ComponentAdmin)
admin.site.register(BinaryRelation, BinaryRelationAdmin)
