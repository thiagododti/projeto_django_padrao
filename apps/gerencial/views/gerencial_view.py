from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.tarefas.models import Checkin
from apps.configuracoes.models import Usuario, Departamento
from django.utils import timezone
from ..functions import *
from django.db.models import Prefetch


@login_required()
def gerencial(request):
    user = request.user

    departamentos_supervisionados = user.departamentos_supervisionados.prefetch_related(
        'departamentos_filhos')
    id_dp_hierarquia = get_departamentos_filhos_recursivo(
        departamentos_supervisionados)

    hoje = timezone.now().date()

    # Base query de funcionarios
    funcionarios_qs = Usuario.objects.filter(
        departamento__id__in=id_dp_hierarquia,
        is_active=True
    )

    # Captura filtros do POST
    if request.method == 'POST':
        filtro = request.POST.get('filtro')
        if filtro:
            empresa_id = request.POST.get('empresa')
            departamento_id = [
                d for d in request.POST.getlist("departamento") if d]

            print(departamento_id)

            if empresa_id:
                funcionarios_qs = funcionarios_qs.filter(
                    departamento__empresa__id=empresa_id)

            if departamento_id:
                funcionarios_qs = funcionarios_qs.filter(
                    departamento__id__in=departamento_id)

    # Prefetch e select_related no final
    funcionarios = (
        funcionarios_qs
        .select_related('cargo')
        .prefetch_related(
            'departamento',
            Prefetch(
                'checkins',
                queryset=Checkin.objects.prefetch_related('tarefas')
            )
        )
        .distinct()
    )

    cards = []
    for func in funcionarios:
        checkins = list(func.checkins.all())

        # Checkin de hoje
        checkin_hoje = next(
            (c for c in checkins if c.data_criacao.date() == hoje), None)
        checkin_status = (
            'fechado' if checkin_hoje and checkin_hoje.concluido
            else 'aberto' if checkin_hoje else 'nao_aberto'
        )

        # Todas tarefas
        todas_tarefas = [t for c in checkins for t in c.tarefas.all()]
        total_tarefas = len(todas_tarefas)
        tarefas_abertas = sum(1 for t in todas_tarefas if not t.concluida)
        reunioes_abertas = sum(
            1 for t in todas_tarefas if t.tipo == 'reuniao' and not t.concluida)
        tarefas_concluidas = total_tarefas - tarefas_abertas
        efetividade = round((tarefas_concluidas / total_tarefas)
                            * 100, 1) if total_tarefas > 0 else 0

        # Lista de nomes de departamentos
        departamentos_nomes = ", ".join(
            d.nome for d in func.departamento.all())

        cards.append({
            'id_func': func.id,
            'nome': func.get_full_name(),
            'cargo': func.cargo.nome if func.cargo else '',
            'departamento': departamentos_nomes,
            'foto': func.photo.url if func.photo else None,
            'efetividade': efetividade,
            'tarefas_abertas': tarefas_abertas,
            'total_tarefas': total_tarefas,
            'reunioes_abertas': reunioes_abertas,
            'checkin_status': checkin_status,
        })

    # Ordenando cards pela efetividade
    cards.sort(key=lambda x: x['efetividade'], reverse=False)

    departamentos = list(
        Departamento.objects
        .filter(id__in=id_dp_hierarquia)
        .select_related('empresa')
    )

    empresas = list({dep.empresa for dep in departamentos})

    context = {
        'user': user,
        'cards': cards,
        'empresas': empresas,
        'departamentos': departamentos
    }

    return render(request, 'gerencial/gerencial.html', context)
