from django.contrib.auth.decorators import login_required
from ..models import Checkin, Tarefa
from django.contrib import messages
from django.shortcuts import render, redirect
from django.db.models import Count, Q, Case, When, IntegerField, Value
from django.core.paginator import Paginator


@login_required
def checkout(request):
    user = request.user

    checkin = (
        Checkin.objects
        .filter(usuario=user, concluido=False)
        .order_by('-data_criacao')
        .first()
    )

    if not checkin:
        messages.warning(request, 'Nenhum check-in ativo encontrado.')
        return redirect('checkin')

    tarefas_qs = (
        Tarefa.objects
        .filter(checkin=checkin)
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

    if not tarefas_qs.exists():
        messages.warning(
            request,
            'Você não possui tarefas neste check-in. '
            'Adicione tarefas antes de finalizar e ser direcionado para sua página de acompanhamento.'
        )
        return redirect('checkin')

    # Paginação
    per_page = request.GET.get("per_page", 6)
    paginator = Paginator(tarefas_qs, per_page)  # tarefas por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # contagens agregadas
    contagens = tarefas_qs.aggregate(
        total=Count('id'),
        concluidas=Count('id', filter=Q(concluida=True)),
        tarefas_nao_planejadas_count=Count(
            Case(When(tipo='nao_planejada', then=1),
                 output_field=IntegerField())
        ),

        reunioes_count=Count(
            Case(When(tipo='reuniao', then=1), output_field=IntegerField())
        ),
    )

    total_tarefas = contagens['total']
    tarefas_concluidas = contagens['concluidas']
    taxa_resolucao = (tarefas_concluidas / total_tarefas *
                      100) if total_tarefas > 0 else 0

    context = {
        'object_list': page_obj,  # compatível com ListView
        'page_obj': page_obj,     # também no estilo ListView
        'is_paginated': page_obj.has_other_pages(),
        'paginator': paginator,

        'checkin': checkin,

        # métricas
        'total_tarefas': total_tarefas,
        'tarefas_concluidas': tarefas_concluidas,
        'tarefas_nao_planejadas_count': contagens['tarefas_nao_planejadas_count'],
        'reunioes': contagens['reunioes_count'],
        'taxa_resolucao': taxa_resolucao,
    }

    return render(request, 'tarefas/checkout.html', context)
