from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.tarefas.models import Checkin, Tarefa


@login_required()
def index(request):
    user = request.user

    checkin = Checkin.objects.filter(
        usuario=user, concluido=False).order_by('-data_criacao').first()

    if not checkin:
        checkin = None

    all_checkins = Checkin.objects.filter(
        usuario=user).order_by('-data_criacao')
    tarefas_planejadas = Tarefa.objects.filter(
        checkin__in=all_checkins).order_by('data_criacao')

    qtd_checkins = all_checkins.count()
    qtd_tarefas_planejadas = tarefas_planejadas.count()
    qtd_tarefas_concluidas = Tarefa.objects.filter(
        checkin__in=all_checkins, concluida=True).count()
    qtd_tarefas_pendentes = qtd_tarefas_planejadas - qtd_tarefas_concluidas
    percentual_tarefas_concluidas = (
        qtd_tarefas_concluidas / qtd_tarefas_planejadas * 100) if qtd_tarefas_planejadas > 0 else 0

    lista_tarefas_hoje = Tarefa.objects.filter(
        checkin__usuario=user,
        checkin__data_criacao__date=checkin.data_criacao.date() if checkin else None,
        concluida=False
    ).order_by('data_criacao')
    context = {
        'user': user,
        'checkin': checkin,
        'tarefas_planejadas': tarefas_planejadas,
        'qtd_checkins': qtd_checkins,
        'qtd_tarefas_planejadas': qtd_tarefas_planejadas,
        'qtd_tarefas_concluidas': qtd_tarefas_concluidas,
        'qtd_tarefas_pendentes': qtd_tarefas_pendentes,
        'percentual_tarefas_concluidas': percentual_tarefas_concluidas,
        'lista_tarefas_hoje': lista_tarefas_hoje,
    }
    # Renderiza a página inicial para usuários autenticados
    return render(request, 'dashboard/index.html', context)
