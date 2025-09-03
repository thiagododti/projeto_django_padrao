from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from ..models import Departamento


@admin.register(Departamento)
class DepartamentoAdmin(admin.ModelAdmin):
    # Colunas visíveis na lista
    list_display = ('nome', 'empresa', 'data_criacao')
    # Pesquisar pelo nome da empresa também
    search_fields = ('nome', 'descricao', 'empresa__nome')
    list_filter = ('empresa', 'data_criacao')  # Filtros laterais
    ordering = ('nome',)
    # Para ManyToManyField ficar em um widget melhor
    filter_horizontal = ('supervisor',)
