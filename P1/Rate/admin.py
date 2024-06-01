from django.contrib import admin
from .models import Rate
# Register your models here.


class DataAdmin(admin.ModelAdmin):
    list_display = ('id', 'rate', 'id_attendance_id')


admin.site.register(Rate, DataAdmin)
