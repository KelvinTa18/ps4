from django.contrib import admin
from .models import Student
# Register your models here.


class DataAdmin(admin.ModelAdmin):
    list_display = ('name', 'gender', 'age', 'number_phone',
                    'address', 'distance', 'predictions', 'id_class')


admin.site.register(Student, DataAdmin)
