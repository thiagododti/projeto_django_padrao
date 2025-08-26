from django import forms
from ..models import Usuario
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from validate_docbr import CPF
# FORM PARA CRIAÇÃO DE NOVO USUÁRIO ATRAVÉS DA TELA DE LOGIN


class RegistrarUsuario(forms.ModelForm):
    password1 = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput(attrs={
            'class': 'w-full bg-white px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500',
            'placeholder': 'Digite sua senha'
        })
    )
    password2 = forms.CharField(
        label="Confirme a Senha",
        widget=forms.PasswordInput(attrs={
            'class': 'w-full bg-white px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500',
            'placeholder': 'Confirme sua senha'
        })
    )

    class Meta:
        model = Usuario
        fields = [
            'username', 'first_name', 'last_name', 'cpf', 'email',
            'data_nascimento', 'data_contratacao', 'photo'
        ]
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500',
                'placeholder': 'Nome de usuário',
                'autocomplete': 'off',
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border bg-white border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500',
                'placeholder': 'Primeiro nome',
                'autocomplete': 'off',

            }),
            'last_name': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border bg-white border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500',
                'placeholder': 'Sobrenome',
                'autocomplete': 'off',
                'required': True
            }),
            'cpf': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border bg-white border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500',
                'placeholder': '000.000.000-00',
                'autocomplete': 'off',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-3 py-2 border bg-white border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500',
                'placeholder': 'seu@email.com',
                'autocomplete': 'off',

            }),
            'data_nascimento': forms.DateInput(attrs={
                'class': 'w-full px-3 py-2 border bg-white border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500',
                'type': 'date',
                'autocomplete': 'off',

            }),
            'data_contratacao': forms.DateInput(attrs={
                'class': 'w-full px-3 py-2 border bg-white border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500',
                'type': 'date',
                'autocomplete': 'off',

            }),
            'photo': forms.FileInput(attrs={
                'class': 'w-full px-3 py-2 border bg-white border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-medium file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100'
            })
        }

    def clean(self):
        cleaned_data = super().clean()

        # Verifica se todos os campos obrigatórios estão preenchidos
        for field in self.Meta.fields + ['password1', 'password2']:
            if not cleaned_data.get(field):
                raise ValidationError(f"O campo '{field}' é obrigatório.")

        return cleaned_data

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if Usuario.objects.filter(username=username).exists():
            raise forms.ValidationError("Este nome de usuário já está em uso.")
        return username

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("As senhas não coincidem.")
        return password2

    def clean_password1(self):
        password = self.cleaned_data.get("password1")
        validate_password(password)
        return password

    def clean_cpf(self):
        cpf_value = self.cleaned_data.get("cpf")
        cpf = CPF()

        if not cpf.validate(cpf_value):
            raise forms.ValidationError("Digite um CPF válido.")

        if Usuario.objects.filter(cpf=cpf_value).exists():
            raise forms.ValidationError("Este CPF já está cadastrado.")

        return cpf_value

    def clean_email(self):
        email = self.cleaned_data.get("email")

        try:
            validate_email(email)
        except ValidationError:
            raise forms.ValidationError("Digite um email válido.")

        if Usuario.objects.filter(email=email).exists():
            raise forms.ValidationError("Este email já está cadastrado.")

        return email
