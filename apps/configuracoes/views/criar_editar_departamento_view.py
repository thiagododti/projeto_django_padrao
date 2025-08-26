from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from ..forms import CriarDepartamentoForm

from ..models import Departamento


@login_required
def criar_departamento_view(request):
    """
    View para criar um novo departamento
    """
    if not request.user.is_superuser:
        raise PermissionDenied()

    if request.method == "POST":
        form = CriarDepartamentoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Departamento criado com sucesso!")
            return redirect("departamentos")
    else:
        form = CriarDepartamentoForm()

    context = {
        'form': form,
        'titulo_departamento': 'Criar Departamento',

    }

    return render(request, 'configuracoes/partials/criar_departamento_form.html', context)


@login_required
def editar_departamento_view(request, departamento_id):
    """
    View para editar um departamento existente
    """
    if not request.user.is_superuser:
        raise PermissionDenied()

    departamento = get_object_or_404(Departamento, id=departamento_id)

    if request.method == "POST":
        form = CriarDepartamentoForm(request.POST, instance=departamento)
        if form.is_valid():
            form.save()
            messages.success(request, "Departamento atualizado com sucesso!")
            return redirect("departamentos")
    else:
        form = CriarDepartamentoForm(instance=departamento)

    context = {
        'form': form,
        'departamento': departamento,
        'titulo_departamento': f'Editar Departamento - {departamento.nome}',

    }

    return render(request, 'configuracoes/partials/criar_departamento_form.html', context)
