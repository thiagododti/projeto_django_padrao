from django import forms
from .models import Empresa


class EmpresaForm(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = '__all__'
        widgets = {
            'cor_primaria': forms.TextInput(attrs={'type': 'color'}),
            'cor_primaria_hover': forms.TextInput(attrs={'type': 'color'}),
            'cor_primaria_texto': forms.TextInput(attrs={'type': 'color'}),
            'cor_secundaria': forms.TextInput(attrs={'type': 'color'}),
            'cor_background': forms.TextInput(attrs={'type': 'color'}),
            'cor_blocos': forms.TextInput(attrs={'type': 'color'}),
            'cor_bordas': forms.TextInput(attrs={'type': 'color'}),
            'cor_texto': forms.TextInput(attrs={'type': 'color'}),
        }
