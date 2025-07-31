from django.contrib import admin
from .models import Empresa
from .forms import EmpresaForm


@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    form = EmpresaForm
    list_display = ('nome', 'cnpj', 'ativo')
