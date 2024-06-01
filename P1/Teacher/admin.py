from django.contrib import admin
from .models import Teacher
# Register your models here.


class DataAdmin(admin.ModelAdmin):
    list_display = ('name', 'age', 'gender', 'number_phone',
                    'address', 'date_created')


admin.site.register(Teacher, DataAdmin)
