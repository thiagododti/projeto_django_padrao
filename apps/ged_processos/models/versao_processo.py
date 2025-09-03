from django.db import models
from ..models import Processo


class VersaoProcesso(models.Model):
    """
    Modelo que representa uma versão de um processo no sistema GED.
    Esta classe armazena informações sobre versões de documentos de processos,
    incluindo o arquivo PDF, links para vídeos relacionados e metadados da versão.
    Attributes:
        processo (Processo): Referência ao processo ao qual esta versão pertence.
        data_criacao (DateTimeField): Data e hora de criação da versão, preenchida automaticamente.
        versao (CharField): Número da versão do processo (ex: '1.0').
        pdf (FileField): Arquivo PDF do processo, opcional.
        url_video (URLField): URL para um vídeo relacionado ao processo, opcional.
        data_versao (DateTimeField): Data e hora da versão, preenchida automaticamente.
    Methods:
        __str__(): Retorna uma string representativa da versão, incluindo o número da versão
                  e o nome do processo.
    """

    processo = models.ForeignKey(
        Processo, on_delete=models.CASCADE, related_name='versoes', verbose_name='Processo')
    # marcar para remover a data_criacao
    data_criacao = models.DateTimeField(
        auto_now_add=True, verbose_name='Data de Criação')
    versao = models.CharField(
        max_length=20, default='1.0', verbose_name='Versão')
    pdf = models.FileField(upload_to='processos_pdfs/',
                           null=True, blank=True, verbose_name='PDF')
    url_video = models.URLField(
        max_length=200, null=True, blank=True, verbose_name='URL do Vídeo')
    data_versao = models.DateTimeField(
        auto_now_add=True, verbose_name='Data da Versão')

    def __str__(self):
        return f"Versão {self.versao} - {self.processo.nome}"
