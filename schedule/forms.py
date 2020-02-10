from django import forms
from .models import SchedFILE


class SchedFILEForm(forms.ModelForm):

    class Meta:
        model = SchedFILE
        fields = ['filename']
