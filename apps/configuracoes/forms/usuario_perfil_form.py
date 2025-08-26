
from django import forms
from ..models import Usuario
from django.forms.widgets import ClearableFileInput
# FORM DA PÁGINA DE PERFIL DO USUÁRIO

# FORM NECESSÁRIO REFATORAR PARA COLOCAR VALIDAÇÕES


class CustomFileInput(ClearableFileInput):
    """Widget customizado para remover texto extra do input de arquivo"""

    # Remove o texto "Currently:" e o link do arquivo
    initial_text = ''
    input_text = ''
    clear_checkbox_label = ''

    def __init__(self, attrs=None):
        super().__init__(attrs)
        # Remove completamente a opção de limpar
        self.clear_checkbox_label = ''

    def format_value(self, value):
        # Retorna apenas o valor sem formatação extra
        if self.is_initial(value):
            return value
        return None

    def render(self, name, value, attrs=None, renderer=None):
        # Renderiza apenas o input file, sem texto adicional
        if attrs is None:
            attrs = {}

        attrs.update(self.attrs)

        # Cria apenas o input file
        file_input = forms.FileInput().render(name, None, attrs, renderer)

        return file_input


class UsuarioPerfil(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = [
            'first_name', 'last_name', 'cpf', 'photo',
            'data_nascimento', 'data_contratacao',
            'cargo'
        ]
        widgets = {
            'data_nascimento': forms.DateInput(
                attrs={'type': 'date'},
                format='%Y-%m-%d'
            ),
            'data_contratacao': forms.DateInput(
                attrs={'type': 'date'},
                format='%Y-%m-%d'
            ),
            'photo': CustomFileInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 file:mr-4 file:py-2 file:px-4 file:rounded-l-lg file:border-0 file:bg-gray-100 hover:file:bg-gray-200 file:text-gray-700',
                'accept': 'image/*'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Configurar os input_formats
        self.fields['data_nascimento'].input_formats = ['%Y-%m-%d']
        self.fields['data_contratacao'].input_formats = ['%Y-%m-%d']

        # Aplicar classes para outros campos
        for field_name, field in self.fields.items():
            if field_name != 'photo':  # Pula o campo photo pois já foi configurado no widget
                field.widget.attrs['class'] = 'w-full px-2 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500'
