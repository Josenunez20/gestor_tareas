from django import forms
from .models import Tarea

class TareaForm(forms.ModelForm):
    class Meta:
        model = Tarea
        fields = ['descripcion', 'fecha_vencimiento']
        labels = {
            'descripcion': '',
            'fecha_vencimiento': ''
        }
        widgets = {
            'descripcion': forms.TextInput(attrs={
                'placeholder': 'Descripción de la tarea',
                'class': 'form-control'
            }),
            'fecha_vencimiento': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
        }