from django.contrib.auth.decorators import login_required

from django.shortcuts import render


@login_required()
def construcao(request):
    context = {

    }
    return render(request, 'construcao.html', context)
