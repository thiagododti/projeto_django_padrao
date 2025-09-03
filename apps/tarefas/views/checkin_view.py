from django.contrib.auth.decorators import login_required
from ..models import Checkin, Tarefa
from django.contrib import messages
from django.shortcuts import render, redirect
from django.db.models import Count, Q, Case, When, IntegerField, Value
from django.core.paginator import Paginator
from django.utils import timezone


@login_required()
def checkin(request):
    user = request.user

    # Busca o último checkin não concluído
    checkin = Checkin.objects.filter(
        usuario=user, concluido=False).order_by('-data_criacao').first()

    # Se não existir, cria um novo checkin
    if not checkin:
        checkin = Checkin.objects.create(
            usuario=user,
            descricao='Checkin criado automaticamente.',
            concluido=False,
            data_criacao=timezone.now()
        )
        tarefas_nao_concluidas = Tarefa.objects.filter(
            checkin__usuario=user, concluida=False)
        for tarefa in tarefas_nao_concluidas:
            tarefa.checkin = checkin
            tarefa.save()

    tarefas_qs = (
        Tarefa.objects
        .filter(checkin=checkin, concluida=False)
        .select_related('origem_tarefa', 'destino_tarefa')
        .annotate(
            prioridade_ordenada=Case(
                When(prioridade='Alta', then=Value(1)),
                When(prioridade='Média', then=Value(2)),
                When(prioridade='Baixa', then=Value(3)),
                default=Value(4),
                output_field=IntegerField(),
            )
        )
        .order_by('concluida', 'prioridade_ordenada')
    )

    # Paginação
    per_page = request.GET.get("per_page", 6)
    paginator = Paginator(tarefas_qs, per_page)  # tarefas por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'object_list': page_obj,  # compatível com ListView
        'page_obj': page_obj,     # também no estilo ListView
        'is_paginated': page_obj.has_other_pages(),
        'paginator': paginator,
    }
    return render(request, 'tarefas/checkin.html', context)
