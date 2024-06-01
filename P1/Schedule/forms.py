from django import forms
from . import models


class SaveForm(forms.ModelForm):

    class Meta:
        model = models.Schedule
        fields = ("date",
                  "check_in", "check_out", "class_id")
