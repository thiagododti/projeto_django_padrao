from django.shortcuts import render
from apps.configuracoes.models import Empresa, Departamento
from ..forms import FiltroProcessosForm
from ..models import Processo, VersaoProcesso
from django.core.paginator import Paginator
from django.db.models import OuterRef, Subquery
from django.db.models.functions import Concat
from django.db.models import F, Value


def index(request):
    form = FiltroProcessosForm(request.POST or None, user=request.user)

    empresa_selecionada = None
    departamento_selecionado = None
    status_selecionado = None
    dono_selecionado = None
    data_atualizacao_selecionada = None

    if form.is_valid():
        empresa_selecionada = form.cleaned_data['empresa']
        departamento_selecionado = form.cleaned_data['departamento']
        status_selecionado = form.cleaned_data['status']
        dono_selecionado = form.cleaned_data['dono']
        data_atualizacao_selecionada = form.cleaned_data['data_atualizacao']

    versao_mais_recente = VersaoProcesso.objects.filter(
        processo=OuterRef('pk')
    ).order_by('-data_versao')

    qs = Processo.objects.annotate(
        versao_atual=Subquery(versao_mais_recente.values('versao')[:1]),
        versao_data=Subquery(versao_mais_recente.values('data_versao')[:1]),
        versao_pdf=Subquery(versao_mais_recente.values('pdf')[:1]),
        versao_url_video=Subquery(versao_mais_recente.values('url_video')[:1]),
    ).select_related('departamento', 'responsavel')

    if empresa_selecionada:
        qs = qs.filter(departamento__empresa=empresa_selecionada)
    if departamento_selecionado:
        qs = qs.filter(departamento=departamento_selecionado)
    if status_selecionado:
        qs = qs.filter(status=status_selecionado)
    if dono_selecionado:
        qs = qs.annotate(
            nome_completo=Concat(F('responsavel__first_name'), Value(' '), F('responsavel__last_name'))).filter(nome_completo__icontains=dono_selecionado)
    if data_atualizacao_selecionada:
        qs = qs.filter(versao_data=data_atualizacao_selecionada)

    paginator = Paginator(qs, 10)
    page_obj = paginator.get_page(request.GET.get("page", 1))

    return render(request, 'ged_processos/index.html', {
        'page_obj': page_obj,
        'form': form,
        'empresa_selecionada': empresa_selecionada,
        'departamento_selecionado': departamento_selecionado,
        'status_selecionado': status_selecionado,
        'dono_selecionado': dono_selecionado,
        'data_atualizacao_selecionada': data_atualizacao_selecionada,
    })
