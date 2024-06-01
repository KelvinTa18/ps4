from django.contrib import admin
from .models import Class
# Register your models here.


class DataAdmin(admin.ModelAdmin):
    list_display = ('name', 'fees', 'id_teacher')


admin.site.register(Class, DataAdmin)
