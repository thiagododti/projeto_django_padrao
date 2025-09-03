from django.db import models
from ..models import Processo
from apps.configuracoes.models import Usuario


class ComentarioProcesso(models.Model):
    """
    Model para comentários em processos no sistema GED.
    Esta classe representa comentários feitos por usuários em processos específicos,
    permitindo o registro de discussões e observações relacionadas aos processos.
    Attributes:
        processo (ForeignKey): Referência ao processo ao qual o comentário pertence.
        usuario (ForeignKey): Usuário que criou o comentário.
        data_criacao (DateTimeField): Data e hora da criação do comentário, preenchida automaticamente.
        conteudo (TextField): Conteúdo textual do comentário.
    """

    processo = models.ForeignKey(
        Processo, on_delete=models.CASCADE, related_name='comentarios', verbose_name='Processo')
    usuario = models.ForeignKey(
        Usuario, on_delete=models.CASCADE, verbose_name='Usuário')
    data_criacao = models.DateTimeField(
        auto_now_add=True, verbose_name='Data da Criação')
    conteudo = models.TextField(
        verbose_name='Conteúdo', blank=False, null=False)

    def __str__(self):
        return f"Comentário de {self.usuario} em {self.processo.nome}"
