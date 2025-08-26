from .models import Configuracao


def empresa(request):
    return {'empresa': Configuracao.configuracao_ativa()}
