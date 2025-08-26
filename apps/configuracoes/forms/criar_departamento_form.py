# forms.py
from django import forms
from ..models import Departamento
from django.contrib.admin.widgets import FilteredSelectMultiple


class CriarDepartamentoForm(forms.ModelForm):
    class Meta:
        model = Departamento
        fields = [
            "nome",
            "descricao",
            "empresa",
            "departamento_pai",
            "supervisor",
        ]
        widgets = {
            "nome": forms.TextInput(attrs={
                "class": "w-full px-3 py-2 border border-gray-300 rounded-xl shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition"
            }),
            "descricao": forms.Textarea(attrs={
                "class": "w-full px-3 py-2 border border-gray-300 rounded-xl shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition",
                "rows": 3,
            }),
            "empresa": forms.Select(attrs={
                "class": "w-full px-3 py-2 border border-gray-300 rounded-xl shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition bg-white"
            }),
            "departamento_pai": forms.Select(attrs={
                "class": "w-full px-3 py-2 border border-gray-300 rounded-xl shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition bg-white"
            }),
            # 🔥 aqui entra TomSelect
            "supervisor": forms.SelectMultiple(attrs={
                "class": "supervisor-select w-full"
            }),
        }
