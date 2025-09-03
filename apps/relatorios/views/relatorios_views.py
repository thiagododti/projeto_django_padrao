from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from apps.tarefas.models import Tarefa
from apps.configuracoes.models import Usuario
from apps.gerencial.functions import get_departamentos_filhos_recursivo
from ..functions import *


@login_required
def relatorio(request):
    # Verificar se o usuário é supervisor
    user = request.user
    departamentos_supervisionados = user.departamentos_supervisionados.prefetch_related(
        'departamentos_filhos')
    is_supervisor = bool(departamentos_supervisionados)

    # Obter IDs dos departamentos supervisionados (incluindo filhos)
    usuarios_supervisionados_ids = []
    if is_supervisor:
        id_dp_hierarquia = get_departamentos_filhos_recursivo(
            departamentos_supervisionados)
        usuarios_supervisionados = Usuario.objects.filter(
            departamento__id__in=id_dp_hierarquia)
        usuarios_supervisionados_ids = list(
            usuarios_supervisionados.values_list('id', flat=True))

    # Query base - se não for supervisor, filtrar apenas as tarefas do usuário
    if is_supervisor:
        tarefas_query = Tarefa.objects.filter(checkin__usuario_id__in=usuarios_supervisionados_ids).select_related(
            'checkin', 'checkin__usuario', 'origem_tarefa', 'destino_tarefa')
    else:
        tarefas_query = Tarefa.objects.filter(checkin__usuario=user).select_related(
            'checkin', 'checkin__usuario', 'origem_tarefa', 'destino_tarefa')

    # Processar filtros se enviados via POST
    filtros_aplicados = {}

    if request.method == 'POST':
        if request.POST.get('acao') in ['filtro', 'exportar']:
            tarefas_query, filtros_aplicados = aplicar_filtros(
                request, tarefas_query, usuarios_supervisionados_ids, is_supervisor)
        if request.POST.get('acao') == 'exportar':
            response = exportar_filtro_excel(tarefas_query, filtros_aplicados)
            return response
    # Ordenar por data de criação do checkin (mais recentes primeiro)
    tarefas_query = tarefas_query.order_by('-checkin__data_criacao')

    # Paginação
    paginator = Paginator(tarefas_query, 15)  # 15 tarefas por página
    page_number = request.GET.get('page')
    tarefas = paginator.get_page(page_number)

    # Lista de usuários para o filtro (apenas para supervisores)
    usuarios_lista = []
    if is_supervisor:
        usuarios_lista = Usuario.objects.filter(
            id__in=usuarios_supervisionados_ids
        ).order_by('first_name', 'last_name')

    context = {
        'tarefas': tarefas,
        'is_supervisor': is_supervisor,
        'usuarios_lista': usuarios_lista,
        'filtros_aplicados': filtros_aplicados,
        'is_paginated': tarefas.has_other_pages(),
        'page_obj': tarefas,
    }

    return render(request, 'relatorios/relatorio.html', context)
