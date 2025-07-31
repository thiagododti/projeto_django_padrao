from .models import Empresa


def empresa(request):
    return {'empresa': Empresa.configuracao_ativa()}
