from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from ..forms import CriarUsuarioForm
from ..models import Usuario


@login_required
def criar_usuario(request):
    user = request.user

    if not user.is_superuser:
        raise PermissionDenied()

    if request.method == 'POST':
        # Usar CriarUsuarioForm para criação (senha obrigatória)
        form = CriarUsuarioForm(request.POST, request.FILES)
        if form.is_valid():
            usuario = form.save()
            messages.success(
                request, f'Usuário "{usuario.username}" criado com sucesso!')
            return redirect('usuarios')  # ou sua URL de lista
        else:
            messages.error(
                request, 'Erro ao criar usuário. Verifique os dados informados.')
    else:
        form = CriarUsuarioForm()

    context = {
        'form': form,
        'titulo_usuario': 'Criar Usuário'
    }

    return render(request, 'configuracoes/partials/criar_usuario_form.html', context)


@login_required
def editar_usuario(request, user_id):
    user = request.user

    if not user.is_superuser:
        raise PermissionDenied()

    usuario = get_object_or_404(Usuario, id=user_id)

    if request.method == 'POST':
        # Usar UsuarioForm para edição (senha opcional)
        form = CriarUsuarioForm(request.POST, request.FILES, instance=usuario)
        if form.is_valid():
            usuario_atualizado = form.save()
            messages.success(
                request, f'Usuário "{usuario_atualizado.username}" atualizado com sucesso!')
            return redirect('usuarios')  # ou sua URL de lista
        else:
            messages.error(
                request, 'Erro ao atualizar usuário. Verifique os dados informados.')
    else:
        form = CriarUsuarioForm(instance=usuario)

    return render(request, 'configuracoes/partials/criar_usuario_form.html', {
        'form': form,
        'usuario': usuario,
        'titulo_usuario': f'Editar Usuário - {usuario.username}'
    })
