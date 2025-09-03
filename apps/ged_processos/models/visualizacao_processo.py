from django.db import models
from ..models import Processo
from apps.configuracoes.models import Usuario


class VisualizacaoProcesso(models.Model):
    """
    Modelo para rastrear visualizações de processos pelos usuários.
    Este modelo registra cada visualização de um processo por um usuário específico,
    armazenando o processo visualizado, o usuário que o visualizou e a data/hora da visualização.
    Attributes:
        processo (Processo): Referência ao processo que foi visualizado.
        usuario (Usuario): Referência ao usuário que visualizou o processo.
        data_visualizacao (DateTimeField): Data e hora em que ocorreu a visualização.
    """
    
    processo = models.ForeignKey(
        Processo, on_delete=models.CASCADE, related_name='visualizacoes', verbose_name='Processo')
    usuario = models.ForeignKey(
        Usuario, on_delete=models.CASCADE, verbose_name='Usuário')
    data_visualizacao = models.DateTimeField(
        auto_now_add=True, verbose_name='Data da Visualização')

    def __str__(self):
        return f"Visualização de {self.usuario} em {self.processo.nome}"
