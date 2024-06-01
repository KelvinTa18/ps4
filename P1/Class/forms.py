from django import forms
from . import models


class SaveForm(forms.ModelForm):

    class Meta:
        model = models.Class
        fields = ("name", "fees", "id_teacher")
