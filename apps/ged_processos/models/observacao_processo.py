from django.db import models
from ..models import Processo
from apps.configuracoes.models import Usuario


class ObservacaoProcesso(models.Model):
    """
    Modelo para armazenar observações relacionadas a processos.
    Esta classe representa observações feitas por usuários sobre processos específicos
    no sistema de gerenciamento de documentos eletrônicos (GED).
    Attributes:
        processo (Processo): Processo ao qual a observação está vinculada.
        usuario (Usuario): Usuário que criou a observação.
        data_criacao (DateTimeField): Data e hora em que a observação foi criada (preenchido automaticamente).
        conteudo (TextField): Conteúdo textual da observação.
    """
    
    processo = models.ForeignKey(
        Processo, on_delete=models.CASCADE, related_name='observacoes', verbose_name='Processo')
    usuario = models.ForeignKey(
        Usuario, on_delete=models.CASCADE, verbose_name='Usuário')
    data_criacao = models.DateTimeField(
        auto_now_add=True, verbose_name='Data da Criação')
    conteudo = models.TextField(
        verbose_name='Conteúdo', blank=False, null=False)

    def __str__(self):
        return f"Observação de {self.usuario} em {self.processo.nome}"
