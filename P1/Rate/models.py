from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.
from django.contrib.auth.models import User as U
from Attendance.models import Attendance

CHOICESRATE = [(2, 'Kurang Puas'), (1, 'Lumayan Puas'), (0, 'Sangat Puas')]


class Rate(models.Model):

    id_attendance = models.ForeignKey(Attendance, on_delete=models.PROTECT)
    rate = models.PositiveIntegerField(choices=CHOICESRATE)

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(U, on_delete=models.PROTECT, default=None)

    def __str__(self):
        return str(self.id_attendance.id_schedule.date)
