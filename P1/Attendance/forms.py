from django import forms
from . import models


class SaveForm(forms.ModelForm):

    class Meta:
        model = models.Attendance
        fields = ("id_schedule", "id_student", "status_attendance")
