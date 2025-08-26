from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from ..forms import CriarEmpresaForm

from ..models import Empresa


@login_required
def criar_empresa_view(request):
    if not request.user.is_superuser:
        raise PermissionDenied()
    if request.method == 'POST':
        form = CriarEmpresaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Empresa criada com sucesso!')
            return redirect('empresas')
    else:
        form = CriarEmpresaForm()

    context = {
        'form': form,
        'titulo': 'Criar Empresa'
    }
    return render(request, 'configuracoes/partials/criar_empresa_form.html', context)


@login_required
def editar_empresa_view(request, empresa_id):
    if not request.user.is_superuser:
        raise PermissionDenied()

    empresa = get_object_or_404(Empresa, id=empresa_id)
    if request.method == 'POST':
        form = CriarEmpresaForm(request.POST, request.FILES, instance=empresa)
        if form.is_valid():
            form.save()
            messages.success(request, 'Empresa atualizada com sucesso!')
            return redirect('empresas')
    else:
        form = CriarEmpresaForm(instance=empresa)
    context = {
        'form': form,
        'titulo': f'Editar Empresa - {empresa.nome}'
    }

    return render(request, 'configuracoes/partials/criar_empresa_form.html', context)
