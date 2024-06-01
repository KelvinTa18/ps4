from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.
from django.contrib.auth.models import User as U
# import joblib
from datetime import datetime
from Class.models import Class

CHOICESGENDER = [(0, 'Woman'), (1, 'Man')]


class Student(models.Model):

    name = models.CharField(max_length=50)
    gender = models.PositiveIntegerField(choices=CHOICESGENDER)
    age = models.PositiveIntegerField(
        validators=[MaxValueValidator(99), MinValueValidator(5)], blank=True
    )
    number_phone = models.CharField(max_length=15)
    address = models.TextField(max_length=50)
    distance = models.PositiveIntegerField()
    predictions = models.CharField(max_length=100, blank=True)
    id_class = models.ForeignKey(Class, on_delete=models.PROTECT)
    date_birth = models.DateField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(U, on_delete=models.PROTECT, default=None)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # ml_model = joblib.load('ml_model/ml_sport_model.joblib')
        # self.predictions = ml_model.predict(
        # [[self.age, self.height, self.sex]])
        self.predictions = ""
        # buat age sendiri
        today = datetime.today()
        self.age = today.year - self.date_birth.year - \
            ((today.month, today.day) <
             (self.date_birth.month, self.date_birth.day))

        return super().save(*args, *kwargs)
