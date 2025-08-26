from django.shortcuts import render
from ..models import Empresa
from django.core.paginator import Paginator
from django.core.exceptions import PermissionDenied


def empresa_list_view(request):
    if not request.user.is_superuser:
        raise PermissionDenied()
    qs = Empresa.objects.all()

    # Filtros
    if request.GET.get("empresa"):
        qs = qs.filter(nome__icontains=request.GET.get("empresa"))

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
        "empresas": page_obj.object_list,  # lista da página atual
        "page_obj": page_obj,             # objeto de paginação para o template
    }
    return render(request, "configuracoes/empresa_list.html", context)
