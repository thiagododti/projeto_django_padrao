from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from models import Usuario


@admin.register(Usuario)
class UsuarioAdmin(BaseUserAdmin):
    model = Usuario
    list_display = ('username', 'cpf', 'email',
                    'cargo', 'is_staff', 'is_active')
    search_fields = ('username', 'cpf', 'email', 'first_name', 'last_name')
    list_filter = ('is_staff', 'is_active', 'cargo')
    ordering = ('username',)

    # Campos que aparecem no formulário de edição/criação
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Informações Pessoais', {'fields': ('first_name', 'last_name',
         'email', 'cpf', 'photo', 'data_nascimento', 'data_contratacao')}),
        ('Departamento & Cargo', {'fields': ('cargo', 'departamento')}),
        ('Permissões', {'fields': ('is_active', 'is_staff',
         'is_superuser', 'groups', 'user_permissions')}),
        ('Datas Importantes', {'fields': ('last_login', 'date_joined')}),
    )

    filter_horizontal = ('departamento', 'groups',
                         'user_permissions')  # Para ManyToMany

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'cpf', 'password1', 'password2', 'is_staff', 'is_active')}
         ),
    )
