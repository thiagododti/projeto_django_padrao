from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from ..forms import CriarCargoForm

from ..models import Cargo


@login_required
def criar_cargo_view(request):
    if not request.user.is_superuser:
        raise PermissionDenied()
    if request.method == "POST":
        form = CriarCargoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Cargo criado com sucesso!")
            return redirect("cargos")
    else:
        form = CriarCargoForm()

    context = {
        "form": form,
        'titulo': 'Criar Cargo'
    }
    return render(request, 'configuracoes/partials/criar_cargo_form.html', context)


@login_required
def editar_cargo_view(request, cargo_id):
    if not request.user.is_superuser:
        raise PermissionDenied()
    cargo = get_object_or_404(Cargo, id=cargo_id)
    if request.method == "POST":
        form = CriarCargoForm(request.POST, instance=cargo)
        if form.is_valid():
            form.save()
            messages.success(request, "Cargo atualizado com sucesso!")
            return redirect("cargos")
    else:
        form = CriarCargoForm(instance=cargo)

    context = {
        "form": form,
        'titulo': f'Editar Cargo - {cargo.nome}'
    }

    return render(request, 'configuracoes/partials/criar_cargo_form.html', context)
