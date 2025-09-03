from django import forms
from apps.configuracoes.models import Empresa, Departamento
from ..models import Processo


class FiltroProcessosForm(forms.Form):
    empresa = forms.ModelChoiceField(
        queryset=Empresa.objects.all(), required=False)
    departamento = forms.ModelChoiceField(
        queryset=Departamento.objects.all(), required=False)
    status = forms.ChoiceField(choices=Processo.status_choices, required=False)
    dono = forms.CharField(max_length=100, required=False)
    data_atualizacao = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        self.fields['empresa'].queryset = Empresa.objects.filter(
            departamentos_por_empresa__usuarios_membros=user).distinct()
        self.fields['departamento'].queryset = Departamento.objects.filter(
            usuarios_membros=user).distinct()
