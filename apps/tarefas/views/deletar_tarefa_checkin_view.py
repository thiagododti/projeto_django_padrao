from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from ..models import Tarefa
from django.core.exceptions import PermissionDenied


@login_required
def deletar_tarefa_checkin(request, tarefa_id):
    tarefa = Tarefa.objects.get(id=tarefa_id)

    if tarefa.checkin.usuario != request.user:
        raise PermissionDenied(
            "Você não tem permissão para acessar os dados deste funcionário.")

    tarefa.delete()

    # volta para a mesma página que fez a requisição
    return redirect(request.META.get('HTTP_REFERER'))
