from django.contrib import admin
from .models import Attendance
# Register your models here.


class DataAdmin(admin.ModelAdmin):
    list_display = ('id_student', 'id_schedule',
                    'status_attendance', 'date_created', 'date_updated')


admin.site.register(Attendance, DataAdmin)
