from django.contrib import admin
from .models import Number


@admin.register(Number)
class NumPlanAdmin(admin.ModelAdmin):
    list_display = ("number", "tenant", "description", "provider", "forward_to")
