from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from apps.tarefas.models import Checkin, Tarefa
from apps.configuracoes.models import Usuario
from django.db.models import Count, Q
from django.db.models import Prefetch
from ..functions import get_departamentos_filhos_recursivo
from django.core.exceptions import PermissionDenied


@login_required()
def dados_funcionario(request, id):
    user = request.user
    # Verificar se o usuário atual é supervisor do funcionário
    departamentos_supervisionados = user.departamentos_supervisionados.all()
    id_dp_hierarquia = get_departamentos_filhos_recursivo(
        departamentos_supervisionados)

    if not Usuario.objects.filter(id=id, departamento__id__in=id_dp_hierarquia).exists():
        raise PermissionDenied(
            "Você não tem permissão para acessar os dados deste funcionário.")

    funcionario = get_object_or_404(
        Usuario.objects.select_related(
            'cargo').prefetch_related('departamento__empresa'),
        id=id
    )

    # Último checkin
    ultimo_checkin = Checkin.objects.filter(
        usuario=funcionario).order_by('-data_criacao').first()

    # Todos checkins com tarefas
    checkins = (
        Checkin.objects.filter(usuario=funcionario)
        .select_related('usuario')
        .prefetch_related(
            Prefetch(
                'tarefas',
                queryset=Tarefa.objects.select_related(
                    'origem_tarefa', 'destino_tarefa')
            )
        )
        .order_by('-data_criacao')
    )

    # Contagens de tarefas
    contagens = Tarefa.objects.filter(checkin__in=checkins).aggregate(
        qtd_tarefas_concluidas=Count('id', filter=Q(concluida=True)),
        qtd_tarefas_pendentes=Count('id', filter=Q(concluida=False)),
        qtd_reunioes_participadas=Count('id', filter=Q(tipo='reuniao')),
    )

    context = {
        'user': user,
        'funcionario': funcionario,
        'ultimo_checkin': ultimo_checkin,
        'checkins': checkins,
        'tarefas_checkins': [t for c in checkins for t in c.tarefas.all()],
        'qtd_checkins': checkins.count(),
        'qtd_tarefas_concluidas': contagens['qtd_tarefas_concluidas'],
        'qtd_tarefas_pendentes': contagens['qtd_tarefas_pendentes'],
        'qtd_reunioes_participadas': contagens['qtd_reunioes_participadas'],
    }
    return render(request, 'gerencial/dados_funcionario.html', context)
