from django import forms
from . import models


class SaveForm(forms.ModelForm):

    class Meta:
        model = models.Rate
        fields = ("id_attendance",
                  "rate")
