from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import make_password
import re
from ..models import Usuario, Cargo, Departamento


class CriarUsuarioForm(UserCreationForm):
    # Campos do User
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-blue-500 focus:border-blue-500',
            'placeholder': 'Digite seu primeiro nome'
        }),
        label='Nome'
    )

    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-blue-500 focus:border-blue-500',
            'placeholder': 'Digite seu sobrenome'
        }),
        label='Sobrenome'
    )

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-blue-500 focus:border-blue-500',
            'placeholder': 'seu.email@exemplo.com'
        }),
        label='E-mail'
    )

    # Campos de permissões
    is_active = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={
            'class': 'h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded'
        }),
        label='Usuário Ativo',
        help_text='Desmarque para desativar o usuário.'
    )

    is_staff = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'h-4 w-4 text-green-600 focus:ring-green-500 border-gray-300 rounded'
        }),
        label='Staff',
        help_text='Permite acesso ao painel administrativo.'
    )

    is_superuser = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'h-4 w-4 text-red-600 focus:ring-red-500 border-gray-300 rounded'
        }),
        label='Superusuário',
        help_text='Concede todos os privilégios administrativos.'
    )

    # Campos personalizados da model Usuario
    cpf = forms.CharField(
        max_length=14,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-blue-500 focus:border-blue-500',
            'placeholder': '000.000.000-00',
            'id': 'cpf-input'
        }),
        label='CPF'
    )

    cargo = forms.ModelChoiceField(
        queryset=Cargo.objects.all(),
        required=False,
        empty_label="Selecione um cargo",
        widget=forms.Select(attrs={
            'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500'
        }),
        label='Cargo'
    )

    departamento = forms.ModelMultipleChoiceField(
        queryset=Departamento.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={
            'class': 'departamento-select w-full'
        }),
        label='Departamentos'
    )

    photo = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500',
            'accept': 'image/*'
        }),
        label='Foto do Usuário'
    )

    data_nascimento = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500',
            'type': 'date'
        }, format='%Y-%m-%d'),
        label='Data de Nascimento'

    )

    data_contratacao = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500',
            'type': 'date'
        }, format='%Y-%m-%d'
        ),
        label='Data de Contratação'
    )

    class Meta:
        model = Usuario
        fields = ('username', 'first_name', 'last_name', 'email', 'is_active', 'is_staff', 'is_superuser',
                  'cpf', 'cargo', 'departamento', 'photo', 'data_nascimento',
                  'data_contratacao', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['data_nascimento'].input_formats = ['%Y-%m-%d']
        self.fields['data_contratacao'].input_formats = ['%Y-%m-%d']
        # Verificar se estamos editando um usuário existente
        is_editing = self.instance and self.instance.pk

        # Estilizar campos herdados do UserCreationForm
        self.fields['username'].widget.attrs.update({
            'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-blue-500 focus:border-blue-500',
            'placeholder': 'Digite um nome de usuário'
        })
        self.fields['username'].label = 'Nome de Usuário'

        # Configurar campos de senha baseado no contexto (criação vs edição)
        if is_editing:
            # Para edição, senha é opcional
            self.fields['password1'].required = False
            self.fields['password2'].required = False
            self.fields['password1'].widget.attrs.update({
                'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-blue-500 focus:border-blue-500',
                'placeholder': 'Deixe em branco para manter a senha atual'
            })
            self.fields['password1'].help_text = 'Deixe em branco se não quiser alterar a senha.'
            self.fields['password1'].label = 'Nova Senha (Opcional)'
        else:
            # Para criação, senha é obrigatória
            self.fields['password1'].widget.attrs.update({
                'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-blue-500 focus:border-blue-500',
                'placeholder': 'Digite a senha'
            })
            self.fields['password1'].label = 'Senha'

        self.fields['password2'].widget.attrs.update({
            'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-blue-500 focus:border-blue-500',
            'placeholder': 'Confirme a senha'
        })
        self.fields['password2'].label = 'Confirmação de Senha'

    def clean_cpf(self):
        cpf = self.cleaned_data.get('cpf')
        if cpf:
            # Remove caracteres não numéricos
            cpf_numbers = re.sub(r'\D', '', cpf)

            # Verifica se tem 11 dígitos
            if len(cpf_numbers) != 11:
                raise ValidationError('CPF deve ter 11 dígitos.')

            # Verifica se não são todos os números iguais
            if cpf_numbers == cpf_numbers[0] * 11:
                raise ValidationError('CPF inválido.')

            # Valida os dígitos verificadores
            if not self._validar_digitos_cpf(cpf_numbers):
                raise ValidationError('CPF inválido.')

            # Verifica duplicação de CPF, excluindo o usuário atual se estiver editando
            if self.instance and self.instance.pk:
                if Usuario.objects.filter(cpf=cpf_numbers).exclude(pk=self.instance.pk).exists():
                    raise ValidationError(
                        'Este CPF já está sendo usado por outro usuário.')
            else:
                if Usuario.objects.filter(cpf=cpf_numbers).exists():
                    raise ValidationError('Este CPF já está sendo usado.')

            return cpf_numbers
        return cpf

    def _validar_digitos_cpf(self, cpf):
        """Valida os dígitos verificadores do CPF"""
        # Primeiro dígito
        soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
        resto = soma % 11
        digito1 = 0 if resto < 2 else 11 - resto

        # Segundo dígito
        soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
        resto = soma % 11
        digito2 = 0 if resto < 2 else 11 - resto

        return cpf[9] == str(digito1) and cpf[10] == str(digito2)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username:
            # Se estamos editando um usuário existente, excluir ele da verificação
            if self.instance and self.instance.pk:
                if Usuario.objects.filter(username=username).exclude(pk=self.instance.pk).exists():
                    raise ValidationError(
                        'Este nome de usuário já está sendo usado.')
            else:
                # Criação de novo usuário
                if Usuario.objects.filter(username=username).exists():
                    raise ValidationError(
                        'Este nome de usuário já está sendo usado.')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            # Se estamos editando um usuário existente, excluir ele da verificação
            if self.instance and self.instance.pk:
                if Usuario.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
                    raise ValidationError('Este e-mail já está sendo usado.')
            else:
                # Criação de novo usuário
                if Usuario.objects.filter(email=email).exists():
                    raise ValidationError('Este e-mail já está sendo usado.')
        return email

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        # Se estamos editando e nenhuma senha foi fornecida, tudo ok
        is_editing = self.instance and self.instance.pk

        if not is_editing:
            # Para criação, senha é obrigatória (UserCreationForm já valida isso)
            pass
        else:
            # Para edição, validar senhas apenas se fornecidas
            if password1 or password2:
                if password1 != password2:
                    raise ValidationError({
                        'password2': 'As senhas não coincidem.'
                    })

        return cleaned_data

    def save(self, commit=True):
        is_editing = self.instance and self.instance.pk

        if is_editing:
            # Para edição, não usar UserCreationForm.save()
            user = super(forms.ModelForm, self).save(commit=False)

            password = self.cleaned_data.get('password1')
            if password:
                user.set_password(password)
            else:
                # Mantém a senha atual
                user.password = self.instance.password
        else:
            # Para criação, aí sim usamos UserCreationForm.save()
            user = super().save(commit=False)

        if commit:
            user.save()
            self.save_m2m()

        return user
