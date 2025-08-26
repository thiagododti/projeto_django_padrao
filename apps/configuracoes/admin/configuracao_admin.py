from django.contrib import admin
from models.configuracao import Configuracao
from forms import ConfiguracaoForm


@admin.register(Configuracao)
class ConfiguracaoAdmin(admin.ModelAdmin):
    form = ConfiguracaoForm
    list_display = ('nome', 'cnpj', 'ativo')
