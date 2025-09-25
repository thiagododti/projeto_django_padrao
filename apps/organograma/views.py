from apps.configuracoes.models import Departamento

from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
# Create your views here.


def organograma(request):
    return render(request, 'organograma/organograma.html')


def organograma_json(request):
    departamentos = Departamento.objects.all()
    data = []

    for dep in departamentos:
        dep_data = {
            'id': dep.id,
            'pid': dep.departamento_pai.id if dep.departamento_pai else None,
            "name": dep.nome,
            # quantidade de membros
            'total_membros': dep.usuarios_membros.count()
        }

        # Loop sobre supervisores
        for idx, supervisor in enumerate(dep.supervisor.all(), start=1):
            dep_data[f"sup_{idx}"] = f"{supervisor.first_name} {supervisor.last_name}".strip(
            )
            dep_data[f"photo_sup_{idx}"] = supervisor.photo.url if supervisor.photo else None

        data.append(dep_data)

    return JsonResponse(data, safe=False)


def departamento_membros_supervisores(request, departamento_id):
    departamento = get_object_or_404(Departamento, id=departamento_id)

    # Função auxiliar para formatar usuário
    def format_usuario(usuario):
        return {
            'id': usuario.id,
            'username': usuario.username,
            'first_name': usuario.first_name,
            'last_name': usuario.last_name,
            'cpf': usuario.cpf,
            'email': usuario.email,
            'photo_url': usuario.photo.url if usuario.photo else None
        }

    membros = [format_usuario(u) for u in departamento.usuarios_membros.all()]
    supervisores = [format_usuario(u) for u in departamento.supervisor.all()]

    return JsonResponse({
        'departamento': departamento.nome,
        'membros': membros,
        'supervisores': supervisores
    })
