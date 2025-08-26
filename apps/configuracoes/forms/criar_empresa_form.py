# forms.py
from django import forms
from ..models import Empresa


class CriarEmpresaForm(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = [
            "nome", "cnpj", "razao_social", "endereco",
            "telefone", "email", "data_fundacao",
            "website", "logo", "status", "cor_empresa"
        ]
        widgets = {
            "nome": forms.TextInput(attrs={
                "class": "w-full px-3 py-2 border border-gray-300 rounded-xl shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition"
            }),
            "cnpj": forms.TextInput(attrs={
                "class": "w-full px-3 py-2 border border-gray-300 rounded-xl shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition",
                "id": "cnpj-input",
                "placeholder": "00.000.000/0000-00"
            }),
            "razao_social": forms.TextInput(attrs={
                "class": "w-full px-3 py-2 border border-gray-300 rounded-xl shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition"
            }),
            "endereco": forms.TextInput(attrs={
                "class": "w-full px-3 py-2 border border-gray-300 rounded-xl shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition"
            }),
            "telefone": forms.TextInput(attrs={
                "class": "w-full px-3 py-2 border border-gray-300 rounded-xl shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition"
            }),
            "email": forms.EmailInput(attrs={
                "class": "w-full px-3 py-2 border border-gray-300 rounded-xl shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition"
            }),
            "data_fundacao": forms.DateInput(attrs={
                "type": "date",
                "class": "w-full px-3 py-2 border border-gray-300 rounded-xl shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition"
            }),
            "website": forms.URLInput(attrs={
                "class": "w-full px-3 py-2 border border-gray-300 rounded-xl shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition"
            }),
            "logo": forms.ClearableFileInput(attrs={
                "class": "block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-xl file:border-0 file:text-sm file:font-semibold file:bg-blue-600 file:text-white hover:file:bg-blue-700"
            }),
            "status": forms.CheckboxInput(attrs={
                "class": "h-5 w-5 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
            }),
            "cor_empresa": forms.TextInput(attrs={
                "type": "color",
                "class": "w-16 h-10 border-0 p-0 rounded"
            }),
        }
