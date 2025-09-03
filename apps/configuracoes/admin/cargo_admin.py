from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from models import Cargo


@admin.register(Cargo)
class CargoAdmin(admin.ModelAdmin):
    # Colunas visíveis na lista
    list_display = ('nome', 'nivel_hierarquico', 'data_criacao')
    # Campos pesquisáveis
    search_fields = ('nome', 'descricao')
    # Filtros laterais
    list_filter = ('nivel_hierarquico', 'data_criacao')
    ordering = ('nivel_hierarquico', 'nome')