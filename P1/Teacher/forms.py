from django import forms
from . import models


class SaveForm(forms.ModelForm):

    class Meta:
        model = models.Teacher
        fields = ("name", "gender", "number_phone", "address", "date_birth")
