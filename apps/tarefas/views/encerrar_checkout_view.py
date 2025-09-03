from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from ..models import Checkin
from django.utils import timezone


@login_required()
def encerrar_checkout(request):
    user = request.user
    checkin = Checkin.objects.filter(
        usuario=user, concluido=False).order_by('-data_criacao').first()

    if checkin:
        checkin.concluido = True
        checkin.data_conclusao = timezone.now()
        checkin.save()
    return redirect('index')
