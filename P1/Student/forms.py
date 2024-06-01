from django import forms
from . import models


class SaveForm(forms.ModelForm):

    class Meta:
        model = models.Student
        fields = ("name",
                  "gender", "number_phone", "address", "distance", "date_birth", "id_class")
