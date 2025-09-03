from datetime import datetime
from openpyxl import Workbook
from django.http import HttpResponse


def aplicar_filtros(request, tarefas_query, usuarios_supervisionados_ids, is_supervisor):
    filtros_aplicados = {}

    # Filtro por usuário
    if is_supervisor and request.POST.get('usuario'):
        usuario_id = int(request.POST.get('usuario'))
        if usuario_id in usuarios_supervisionados_ids:
            tarefas_query = tarefas_query.filter(
                checkin__usuario_id=usuario_id)
            filtros_aplicados['usuario'] = usuario_id

    # Data inicial
    if request.POST.get('data_inicial'):
        try:
            data_inicial_obj = datetime.strptime(
                request.POST.get('data_inicial'), '%Y-%m-%d').date()
            tarefas_query = tarefas_query.filter(
                checkin__data_criacao__date__gte=data_inicial_obj)
            filtros_aplicados['data_inicial'] = request.POST.get(
                'data_inicial')
        except ValueError:
            pass

    # Data final
    if request.POST.get('data_final'):
        try:
            data_final_obj = datetime.strptime(
                request.POST.get('data_final'), '%Y-%m-%d').date()
            tarefas_query = tarefas_query.filter(
                checkin__data_criacao__date__lte=data_final_obj)
            filtros_aplicados['data_final'] = request.POST.get('data_final')
        except ValueError:
            pass

    # Status
    if request.POST.get('status'):
        status = request.POST.get('status')
        if status == 'concluido':
            tarefas_query = tarefas_query.filter(concluida=True)
        elif status == 'pendente':
            tarefas_query = tarefas_query.filter(concluida=False)
        filtros_aplicados['status'] = status

    # Tipo
    if request.POST.get('tipo'):
        tipo = request.POST.get('tipo')
        tarefas_query = tarefas_query.filter(tipo=tipo)
        filtros_aplicados['tipo'] = tipo

    # Prioridade
    if request.POST.get('prioridade'):
        prioridade = request.POST.get('prioridade')
        tarefas_query = tarefas_query.filter(prioridade=prioridade)
        filtros_aplicados['prioridade'] = prioridade

    return tarefas_query, filtros_aplicados


def exportar_filtro_excel(tarefas_query, filtros_aplicados):
    # aqui sim vai exportar a query já filtrada
    wb = Workbook()
    ws = wb.active
    ws.title = "Relatório de Tarefas"
    ws.append(["Usuário", "Data Checkin", "Origem", "Destino", "Tipo", "Titulo", "Horas Estimadas",
              "Prioridade", "Status", "Cliente Tarefa", "Data Inicio", "Data Conclusão", "Solicitacao Diretoria", "Departamento Tarefa"])
    for tarefa in tarefas_query:
        ws.append([
            f"{tarefa.checkin.usuario.first_name} {tarefa.checkin.usuario.last_name}",
            tarefa.checkin.data_criacao.strftime("%d/%m/%Y %H:%M"),
            tarefa.origem_tarefa.nome if tarefa.origem_tarefa else "-",
            tarefa.destino_tarefa.nome if tarefa.destino_tarefa else "-",
            tarefa.tipo,
            tarefa.titulo if tarefa.titulo else "-",
            tarefa.horas_estimadas,
            tarefa.prioridade,
            tarefa.concluida and "Concluída" or "Pendente",
            tarefa.cliente_tarefa if tarefa.cliente_tarefa else "-",
            tarefa.data_inicio_real.strftime(
                "%d/%m/%Y %H:%M") if tarefa.data_inicio_real else "-",
            tarefa.data_conclusao_real.strftime(
                "%d/%m/%Y %H:%M") if tarefa.data_conclusao_real else "-",
            tarefa.solicitacao_diretoria and "Sim" or "Não",
            tarefa.tarefa_departamento.nome if tarefa.tarefa_departamento else "-"
        ])

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    if 'usuario' in filtros_aplicados:
        nome_arquivo = f"relatorio_tarefas_{tarefas_query[0].checkin.usuario.username}.xlsx"
    else:
        nome_arquivo = "relatorio_tarefas_geral.xlsx"

    response['Content-Disposition'] = f'attachment; filename={nome_arquivo}'
    wb.save(response)

    return response
