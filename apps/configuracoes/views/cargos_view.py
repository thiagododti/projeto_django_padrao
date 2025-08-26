from django.shortcuts import render
from ..models import Cargo
from django.core.paginator import Paginator
from django.core.exceptions import PermissionDenied


def cargo_list_view(request):
    if not request.user.is_superuser:
        raise PermissionDenied()

    qs = Cargo.objects.all()

    # Filtros
    if request.GET.get("cargo"):
        qs = qs.filter(nome__icontains=request.GET.get("cargo"))

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
        "cargos": page_obj.object_list,  # lista da página atual
        "page_obj": page_obj,             # objeto de paginação para o template
    }
    return render(request, "configuracoes/cargo_list.html", context)
