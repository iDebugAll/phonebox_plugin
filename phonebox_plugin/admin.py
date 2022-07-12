from django.contrib import admin
from .models import Number


@admin.register(Number)
class NumPlanAdmin(admin.ModelAdmin):
    list_display = ('number', 'fio', 'pbx', 'tenant', 'region', 'site', 'provider')
