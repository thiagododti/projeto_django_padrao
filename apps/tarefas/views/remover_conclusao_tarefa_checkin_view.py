from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from ..models import Tarefa
from django.core.exceptions import PermissionDenied


@login_required()
def remover_conclusao_tarefa_checkin(request, tarefa_id):
    tarefa = Tarefa.objects.get(id=tarefa_id)
    if not tarefa.checkin.usuario == request.user:
        raise PermissionDenied(
            "Você não tem permissão para acessar os dados deste funcionário.")
    else:
        tarefa.concluida = False
        tarefa.data_conclusao = None
        tarefa.save()
        return redirect('checkout')
