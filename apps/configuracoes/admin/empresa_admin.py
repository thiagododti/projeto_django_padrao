from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from models import Empresa


@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cnpj', 'razao_social', 'status',
                    'data_cadastro')  # Colunas visíveis
    search_fields = ('nome', 'cnpj', 'razao_social', 'email',
                     'telefone')        # Campos pesquisáveis
    # Filtros laterais
    list_filter = ('status', 'data_cadastro')
    ordering = ('nome',)
    readonly_fields = ('data_cadastro', 'data_atualizacao')
