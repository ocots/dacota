from django.contrib import admin

from .models import BinaryRelation, Component

# Register your models here.


class ComponentAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "a", "b", "c")


class BinaryRelationAdmin(admin.ModelAdmin):
    list_display = ("component1", "component2", "a12", "a21", "alpha")
    # filter_horizontal = ("components",)


admin.site.register(Component, ComponentAdmin)
admin.site.register(BinaryRelation, BinaryRelationAdmin)
