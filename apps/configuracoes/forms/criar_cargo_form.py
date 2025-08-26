# forms.py
from django import forms
from ..models import Cargo
from django.contrib.admin.widgets import FilteredSelectMultiple


class CriarCargoForm(forms.ModelForm):
    class Meta:
        model = Cargo
        fields = ["nome", "descricao", "nivel_hierarquico"]
        widgets = {
            "nome": forms.TextInput(attrs={
                "class": "w-full px-3 py-2 border border-gray-300 rounded-xl shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition"
            }),
            "descricao": forms.Textarea(attrs={
                "class": "w-full px-3 py-2 border border-gray-300 rounded-xl shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition",
                "rows": 4
            }),
            "nivel_hierarquico": forms.NumberInput(attrs={
                "class": "w-full px-3 py-2 border border-gray-300 rounded-xl shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition",
                "min": 1
            }),
        }
