from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.
from django.contrib.auth.models import User as U
from Teacher.models import Teacher


class Class(models.Model):

    name = models.CharField(max_length=50)
    fees = models.PositiveIntegerField()
    id_teacher = models.ForeignKey(Teacher, on_delete=models.PROTECT)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(U, on_delete=models.PROTECT, default=None)

    def __str__(self):
        return self.name
