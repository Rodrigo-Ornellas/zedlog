from django import forms
from .models import PortFILE


class PortFILEForm(forms.ModelForm):
    # date = DateField(widget=DateInput(format='%d/%m/%Y'),
    #                  input_formats=('%d/%m/%Y',))
    class Meta:
        model = PortFILE
        fields = ['filename']
