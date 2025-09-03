from ..models import Tarefa
from apps.configuracoes.models import Empresa, Usuario
from django import forms
from django.utils import timezone


class TarefaForm(forms.ModelForm):
    class Meta:
        model = Tarefa
        fields = ['titulo', 'concluida', 'tipo',  'prioridade', 'descricao', 'horas_estimadas',
                  'origem_tarefa', 'destino_tarefa', 'cliente_tarefa', 'solicitacao_diretoria',
                  'tarefa_departamento', 'data_inicio_real', 'data_conclusao_real', 'observacoes']
        widgets = {
            'checkin': forms.Select(
                attrs={"class": "form-select w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-transparent focus:ring-2 focus:ring-blue-500 focus:outline-none", }
            ),
            'horas_estimadas': forms.TextInput(
                attrs={"placeholder": "HH:MM:SS",
                       "class": "time-input w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-transparent focus:ring-2 focus:ring-blue-500 focus:outline-none", }
            ),
            'tipo': forms.Select(
                attrs={"class": "form-select w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-transparent focus:ring-2 focus:ring-blue-500 focus:outline-none"}
            ),
            'titulo': forms.TextInput(
                attrs={"class": "form-input w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-transparent focus:ring-2 focus:ring-blue-500 focus:outline-none",
                       "maxlength": "200",
                       "required": "required"
                       }
            ),
            'descricao': forms.Textarea(
                attrs={"class": "form-input w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-transparent focus:ring-2 focus:ring-blue-500 focus:outline-none",
                       "required": "required",
                       "rows": 3,
                       "placeholder": "Adicione aqui uma descrição detalhada da tarefa"
                       }
            ),
            'observacoes': forms.Textarea(
                attrs={"class": "form-input w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-transparent focus:ring-2 focus:ring-blue-500 focus:outline-none",
                       "rows": 3,
                       "placeholder": "Adicione aqui observações ou atualizações sobre a tarefa ou justificativas sobre qualquer ocorrido"
                       }
            ),
            'prioridade': forms.Select(
                attrs={"class": "form-select w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-transparent focus:ring-2 focus:ring-blue-500 focus:outline-none",
                       "required": "required",
                       }
            ),
            'origem_tarefa': forms.Select(
                attrs={"class": "form-select w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-transparent focus:ring-2 focus:ring-blue-500 focus:outline-none"}
            ),
            'destino_tarefa': forms.Select(
                attrs={"class": "form-select w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-transparent focus:ring-2 focus:ring-blue-500 focus:outline-none",
                       "required": "required",
                       }
            ),
            'cliente_tarefa': forms.TextInput(
                attrs={"class": "form-select w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-transparent focus:ring-2 focus:ring-blue-500 focus:outline-none",
                       "placeholder": "Preencha o cliente se a tarefa for para um cliente específico"}
            ),
            'concluida': forms.CheckboxInput(
                attrs={
                    "class": "form-checkbox h-6 w-6 text-blue-600 border-gray-300 rounded focus:ring-blue-500"}
            ),
            'solicitacao_diretoria': forms.CheckboxInput(
                attrs={
                    "class": "form-checkbox h-6 w-6 text-blue-600 border-gray-300 rounded focus:ring-blue-500"}
            ),
            'tarefa_departamento': forms.Select(
                attrs={"class": "form-select w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-transparent focus:ring-2 focus:ring-blue-500 focus:outline-none",
                       "required": "required", }
            ),
            'data_inicio_real': forms.DateTimeInput(
                attrs={
                    "type": "datetime-local",  # <- Isso faz o campo virar date+time nativo
                    "class": "form-input w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-transparent focus:ring-2 focus:ring-blue-500 focus:outline-none",
                    "placeholder": "Data de Início Real",
                    "required": "required"

                },
                format="%Y-%m-%dT%H:%M",  # <- importante para o HTML5 datetime-local

            ),
            'data_conclusao_real': forms.DateTimeInput(
                attrs={
                    "type": "datetime-local",
                    "class": "form-input w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-transparent focus:ring-2 focus:ring-blue-500 focus:outline-none",
                    "placeholder": "Data de Conclusão Real"
                },
                format="%Y-%m-%dT%H:%M",
            ),
        }

    def __init__(self, *args, **kwargs):
        usuario = kwargs.pop('usuario', None)
        checkin = kwargs.pop('checkin', None)
        checkout = kwargs.pop('checkout', False)
        conclusao = kwargs.pop('conclusao', False)
        super().__init__(*args, **kwargs)

        current_tipo = getattr(self.instance, 'tipo', None)

        # ---------- Configurações do usuário ----------
        if usuario:
            # Empresas dos departamentos do usuário
            empresas = Empresa.objects.filter(
                departamentos_por_empresa__usuarios_membros=usuario
            ).distinct()
            self.fields['origem_tarefa'].queryset = empresas
            if empresas.exists():
                self.fields['origem_tarefa'].initial = empresas.first().id

            self.fields['tarefa_departamento'].queryset = usuario.departamento.all()

        # ---------- Checkin ----------
        if checkin:
            self.instance.checkin_id = checkin

        # ---------- Checkout ----------
        if checkout:
            # Novo registro: remove "planejada" das choices
            if not self.instance.pk:
                self.fields['tipo'].choices = [
                    (value, label) for value, label in self.fields['tipo'].choices
                    if value != 'planejada'
                ]
            else:
                # Edição: mantém "planejada" se já estava selecionada
                if current_tipo == 'planejada':
                    self.fields['tipo'].choices = [
                        (value, label) for value, label in self.fields['tipo'].choices
                        if value != 'planejada'
                    ] + [('planejada', 'Planejada')]

        # ---------- Edição ----------
        if self.instance.pk:
            # Desabilita o campo tipo ao editar
            self.fields['tipo'].disabled = True

        # ---------- Conclusão ----------
        if conclusao:
            self.fields['data_conclusao_real'].required = True
            self.fields['concluida'].required = True

    def save(self, commit=True):
        instance = super().save(commit=False)

        # If the task is marked as completed, set the completion date to now
        if instance.concluida:
            instance.data_conclusao = timezone.now()
        # If the task is marked as not completed, clear the completion date
        else:
            instance.data_conclusao = None

        if commit:
            instance.save()
        return instance
