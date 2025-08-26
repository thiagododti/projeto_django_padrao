from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from ..models import Usuario, Cargo, Departamento
from django.core.exceptions import PermissionDenied


@login_required(login_url='/login/')
def usuario_list_view(request):
    if not request.user.is_superuser:
        raise PermissionDenied()
    # ---------------------
    # Tratar filtro GET
    # ---------------------
    qs = Usuario.objects.select_related(
        "cargo").prefetch_related("departamento").all().order_by("first_name", "last_name")
    nome = request.GET.get("nome")
    cpf = request.GET.get("cpf")
    cargo = request.GET.get("cargo")
    departamento = request.GET.get("departamento")

    if nome:
        qs = qs.filter(Q(first_name__icontains=nome)
                       | Q(last_name__icontains=nome))
    if cpf:
        qs = qs.filter(cpf__icontains=cpf)
    if cargo:
        qs = qs.filter(cargo__nome__iexact=cargo)
    if departamento:
        qs = qs.filter(departamento__nome__iexact=departamento)

    # ---------------------
    # Paginação
    # ---------------------
    page_number = request.GET.get("page", 1)
    paginator = Paginator(qs, 10)  # 10 itens por página
    page_obj = paginator.get_page(page_number)

    # ---------------------
    # Contexto do template
    # ---------------------
    context = {
        "usuarios": page_obj.object_list,  # lista da página atual
        "page_obj": page_obj,             # objeto de paginação para o template
        "cargos": Cargo.objects.all(),
        "departamentos": Departamento.objects.all(),

    }

    return render(request, "configuracoes/usuario_list.html", context)
