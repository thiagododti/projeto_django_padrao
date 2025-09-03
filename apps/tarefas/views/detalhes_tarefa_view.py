from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse
from ..models import Tarefa
from django.contrib.auth.decorators import login_required


@login_required
def detalhes_tarefa(request, tarefa_id):
    tarefa = get_object_or_404(Tarefa, id=tarefa_id)

    # if tarefa.checkin.usuario != request.user:
    #     return JsonResponse(
    #         {"error": "Você não tem permissão para ver os detalhes desta tarefa."},
    #         status=403
    #     )

    return JsonResponse({
        "id": tarefa.id,
        "titulo": tarefa.titulo,
        "tipo": getattr(tarefa, "tipo", None),
        "descricao": getattr(tarefa, "descricao", None),
        "data_criacao": tarefa.data_criacao.strftime("%d/%m/%Y %H:%M") if tarefa.data_criacao else None,
        "data_conclusao": tarefa.data_conclusao.strftime("%d/%m/%Y %H:%M") if tarefa.data_conclusao else None,
        "observacoes": getattr(tarefa, "observacoes", None),
        "horas_estimadas": getattr(tarefa, "horas_estimadas", None),
        "prioridade": getattr(tarefa, "prioridade", None),
        "concluida": "Concluída" if getattr(tarefa, "concluida", False) else "Pendente",
        "checkin_id": tarefa.checkin.id,
        "cliente_tarefa": getattr(tarefa, "cliente_tarefa", None),
    })
