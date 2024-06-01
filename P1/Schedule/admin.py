from django.contrib import admin
from .models import Schedule
# Register your models here.


class DataAdmin(admin.ModelAdmin):
    list_display = ('date', 'check_in', 'check_out')


admin.site.register(Schedule, DataAdmin)
