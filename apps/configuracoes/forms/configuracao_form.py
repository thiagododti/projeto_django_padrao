from django import forms
from ..models import Configuracao


class ConfiguracaoForm(forms.ModelForm):
    class Meta:
        model = Configuracao
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
            'cor_texto_hover': forms.TextInput(attrs={'type': 'color'}),
        }
