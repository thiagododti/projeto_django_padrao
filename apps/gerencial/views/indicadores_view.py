
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.configuracoes.models import Empresa, Departamento, Usuario
from apps.tarefas.models import Tarefa
import json
from datetime import datetime, date
from ..functions import *


@login_required()
def indicadores(request):
    user = request.user

    departamentos_supervisionados = user.departamentos_supervisionados.prefetch_related(
        'departamentos_filhos')
    id_dp_hierarquia = get_departamentos_filhos_recursivo(
        departamentos_supervisionados)
    # Base query de funcionarios
    funcionarios_qs = Usuario.objects.filter(
        departamento__id__in=id_dp_hierarquia,
        is_active=True
    )

    lista_empresas = Empresa.objects.all().values('id', 'nome').filter(
        id__in=funcionarios_qs.values('departamento__empresa__id')
    )
    lista_departamentos = Departamento.objects.all().values('id', 'nome').filter(
        id__in=funcionarios_qs.values('departamento__id')
    )

    if request.method == 'POST':
        print(request.POST.getlist("departamento"))
        # aplicar filtros do POST
        data_inicio = request.POST.get('data_inicio')
        data_fim = request.POST.get('data_fim')
        departamentos = [d for d in request.POST.getlist("departamento") if d]
        empresa = request.POST.get('empresa')
        concluida = request.POST.get('concluida')
    else:
        # nenhum filtro -> pega todos os dados

        # Get first and last day of current month
        current_date = datetime.now()
        data_inicio = date(current_date.year,
                           current_date.month, 1).strftime('%Y-%m-%d')
        # Get last day by getting first day of next month and subtracting one day
        if current_date.month == 12:
            data_fim = date(current_date.year + 1, 1,
                            1).replace(day=1).strftime('%Y-%m-%d')
        else:
            data_fim = date(current_date.year,
                            current_date.month + 1, 1).strftime('%Y-%m-%d')
        empresa = concluida = None
        departamentos = []
    print(departamentos)
    # Query tarefas
    tarefas = Tarefa.objects.all().select_related('checkin', 'checkin__usuario').prefetch_related(
        'checkin__usuario__departamento__empresa'
    ).filter(
        checkin__usuario__id__in=funcionarios_qs.values('id')
    )

    # aplicar filtros somente se vierem
    if data_inicio:
        tarefas = tarefas.filter(data_criacao__gte=data_inicio)
    if data_fim:
        tarefas = tarefas.filter(data_criacao__lte=data_fim)
    if departamentos:

        print(departamentos)
        tarefas = tarefas.filter(
            checkin__usuario__departamento__id__in=departamentos)
    if empresa:
        tarefas = tarefas.filter(
            checkin__usuario__departamento__empresa__nome__icontains=empresa)
    if concluida is not None:
        tarefas = tarefas.filter(concluida=concluida)

    tarefas = tarefas.distinct()

    # Calcular percentual de conclusão por usuário
    usuarios = {}
    for tarefa in tarefas:
        usuario = tarefa.checkin.usuario
        usuario_id = usuario.id
        nome_usuario = f"{usuario.first_name} {usuario.last_name}".strip(
        ) or usuario.username

        if usuario_id not in usuarios:
            usuarios[usuario_id] = {
                'url_foto': usuario.photo.url if usuario.photo else None,
                'nome': nome_usuario,
                'total': 0,
                'concluidas': 0
            }

        usuarios[usuario_id]['total'] += 1
        if tarefa.concluida:
            usuarios[usuario_id]['concluidas'] += 1

    percentual_conclusao = []
    for usuario_id, dados in usuarios.items():
        total = dados['total']
        concluidas = dados['concluidas']
        percentual = (concluidas / total * 100) if total > 0 else 0
        percentual_conclusao.append({
            'url_foto': dados['url_foto'],
            'usuario_id': usuario_id,
            'nome': dados['nome'],
            'total_tarefas': total,
            'tarefas_concluidas': concluidas,
            'percentual': round(percentual, 2)
        })
    filtros = {
        'data_inicio': data_inicio,
        'data_fim': data_fim,
        'empresa': empresa,
        'departamentos': departamentos,  # lista de IDs
    }

    return render(request, 'gerencial/indicadores.html', {
        'lista_empresas': lista_empresas,
        'lista_departamentos': lista_departamentos,
        'dados_percentual': percentual_conclusao,
        'json_dados_percentual': json.dumps(percentual_conclusao),
        'filtros': filtros
    })
