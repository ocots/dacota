from django.contrib import admin

from .models import BinaryRelation, Component

# Register your models here.
admin.site.register(Component)
admin.site.register(BinaryRelation)
