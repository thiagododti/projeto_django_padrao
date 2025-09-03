from apps.tarefas.forms import TarefaForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from apps.tarefas.models import Checkin, Tarefa
from django.core.exceptions import PermissionDenied


@login_required
def criar_tarefa_checkin(request):
    titulo_header = "Criar Tarefa"
    titulo_botao = "Criar Tarefa"
    usuario = request.user

    # Busca o último checkin não concluído
    checkin = Checkin.objects.filter(
        usuario=usuario, concluido=False).order_by('-data_criacao').first()

    if not checkin:
        # Se não houver checkin ativo, redireciona para a página de inicio
        return redirect('index')

    if request.method == 'POST':
        form_tarefa_checkin = TarefaForm(
            request.POST, usuario=usuario, checkin=checkin.id)
        if form_tarefa_checkin.is_valid():
            form_tarefa_checkin.save()
            return redirect('checkin')
    else:
        form_tarefa_checkin = TarefaForm(
            usuario=usuario, checkin=checkin.id)

    context = {
        'form_tarefa_checkin': form_tarefa_checkin,
        'titulo_header': titulo_header,
        'titulo_botao': titulo_botao
    }

    return render(request, 'tarefas/form_html/tarefa_checkin.html', context)


@login_required
def editar_tarefa_checkin(request, tarefa_id):
    usuario = request.user
    titulo_header = "Atualizar Tarefa"
    titulo_botao = "Atualizar Tarefa"
    tarefa = Tarefa.objects.get(id=tarefa_id)

    if tarefa.checkin.usuario != request.user:
        raise PermissionDenied(
            "Você não tem permissão para acessar os dados deste funcionário.")

    if request.method == 'POST':
        form_tarefa_checkin = TarefaForm(
            request.POST, instance=tarefa, usuario=usuario)
        if form_tarefa_checkin.is_valid():
            form_tarefa_checkin.save()
            return redirect('checkin')
    else:
        form_tarefa_checkin = TarefaForm(
            instance=tarefa, usuario=usuario)

    context = {
        'form_tarefa_checkin': form_tarefa_checkin,
        'titulo_header': titulo_header,
        'titulo_botao': titulo_botao
    }

    return render(request, 'tarefas/form_html/tarefa_checkin.html', context)


@login_required
def criar_tarefa_checkout(request):
    titulo_header = "Criar Tarefa"
    titulo_botao = "Criar Tarefa"
    usuario = request.user

    # Busca o último checkin não concluído
    checkin = Checkin.objects.filter(
        usuario=usuario, concluido=False).order_by('-data_criacao').first()

    if not checkin:
        # Se não houver checkin ativo, redireciona para a página de inicio
        return redirect('index')

    if request.method == 'POST':
        form_tarefa_checkin = TarefaForm(
            request.POST, usuario=usuario, checkin=checkin.id, checkout=True)
        if form_tarefa_checkin.is_valid():
            form_tarefa_checkin.save()
            return redirect('checkout')
    else:
        form_tarefa_checkin = TarefaForm(usuario=usuario, checkout=True)

    context = {
        'form_tarefa_checkin': form_tarefa_checkin,
        'titulo_header': titulo_header,
        'titulo_botao': titulo_botao
    }

    return render(request, 'tarefas/form_html/tarefa_checkin.html', context)


@login_required
def editar_tarefa_checkout(request, tarefa_id):
    usuario = request.user
    titulo_header = "Atualizar Tarefa"
    titulo_botao = "Atualizar Tarefa"

    tarefa = Tarefa.objects.get(id=tarefa_id)

    if tarefa.checkin.usuario != request.user:
        raise PermissionDenied(
            "Você não tem permissão para acessar os dados deste funcionário.")

    if request.method == 'POST':
        form_tarefa_checkin = TarefaForm(
            request.POST, instance=tarefa, usuario=usuario, checkout=True)
        if form_tarefa_checkin.is_valid():
            form_tarefa_checkin.save()
            return redirect('checkout')
    else:
        form_tarefa_checkin = TarefaForm(
            instance=tarefa, usuario=usuario, checkout=True)

    context = {
        'form_tarefa_checkin': form_tarefa_checkin,
        'titulo_header': titulo_header,
        'titulo_botao': titulo_botao
    }

    return render(request, 'tarefas/form_html/tarefa_checkin.html', context)


@login_required
def concluir_tarefa_checkout(request, tarefa_id):
    usuario = request.user
    titulo_header = "Concluir Tarefa"
    titulo_botao = "Concluir Tarefa"

    tarefa = Tarefa.objects.get(id=tarefa_id)

    if tarefa.checkin.usuario != request.user:
        raise PermissionDenied(
            "Você não tem permissão para acessar os dados deste funcionário.")

    if request.method == 'POST':
        form_tarefa_checkin = TarefaForm(
            request.POST, instance=tarefa, usuario=usuario, conclusao=True, checkout=True)

        if form_tarefa_checkin.is_valid():

            form_tarefa_checkin.save()
            return redirect('checkout')
        else:
            print(form_tarefa_checkin.errors)
    else:
        form_tarefa_checkin = TarefaForm(
            instance=tarefa, usuario=usuario, conclusao=True, checkout=True)

    context = {
        'form_tarefa_checkin': form_tarefa_checkin,
        'titulo_header': titulo_header,
        'titulo_botao': titulo_botao
    }

    return render(request, 'tarefas/form_html/tarefa_checkin.html', context)
