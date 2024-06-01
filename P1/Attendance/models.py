from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.
from django.contrib.auth.models import User as U
from Student.models import Student
from Schedule.models import Schedule

CHOICESATTENDACE = [(0, 'Absent'), (1, 'Present')]


class Attendance(models.Model):

    id_schedule = models.ForeignKey(Schedule, on_delete=models.PROTECT)
    id_student = models.ForeignKey(Student, on_delete=models.PROTECT)
    status_attendance = models.PositiveIntegerField(choices=CHOICESATTENDACE)

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(U, on_delete=models.PROTECT, default=None)

    def __str__(self):
        return str(self.id_schedule.date)

    class Meta:
        # Definisikan kombinasi unik dari tabel_a dan tabel_b untuk mencegah duplikat
        unique_together = ('id_schedule', 'id_student')
        default_permissions = ('add', 'change', 'delete')
        permissions = (
            ('list_attendance', 'can update list attendance'),
        )
