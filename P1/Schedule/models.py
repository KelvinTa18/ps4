from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.
from django.contrib.auth.models import User as U
# import joblib
from datetime import datetime
from Class.models import Class


class Schedule(models.Model):

    date = models.DateField()
    check_in = models.TimeField()
    check_out = models.TimeField()
    class_id = models.ForeignKey(Class, on_delete=models.PROTECT)

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(U, on_delete=models.PROTECT, default=None)

    def __str__(self):
        return str(self.date)

    def save(self, *args, **kwargs):

        # cek checkin dan checkout
        if self.check_in > self.check_out:
            # Swap check_in and check_out
            self.check_in, self.check_out = self.check_out, self.check_in

        return super().save(*args, *kwargs)
