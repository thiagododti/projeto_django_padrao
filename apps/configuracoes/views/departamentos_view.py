from django.shortcuts import render
from ..models import Departamento
from django.core.paginator import Paginator
from django.core.exceptions import PermissionDenied


def departamento_list_view(request):
    if not request.user.is_superuser:
        raise PermissionDenied()
    qs = Departamento.objects.all().select_related(
        'empresa')

    # Filtros
    if request.GET.get("departamento"):
        qs = qs.filter(nome__icontains=request.GET.get("departamento"))
    if request.GET.get("empresa"):
        qs = qs.filter(empresa__nome__icontains=request.GET.get("empresa"))
    if request.GET.get("dep_pai"):
        qs = qs.filter(
            departamento_pai__nome__icontains=request.GET.get("dep_pai"))

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
        "departamentos": page_obj.object_list,  # lista da página atual
        "page_obj": page_obj,             # objeto de paginação para o template
    }
    return render(request, "configuracoes/departamento_list.html", context)
