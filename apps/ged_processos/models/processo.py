from django.db import models
from apps.configuracoes.models import Departamento
from apps.configuracoes.models import Usuario

# Create your models here.


class Processo(models.Model):
    """
    Modelo para representar processos no sistema de Gestão Eletrônica de Documentos (GED).
    Este modelo armazena informações sobre processos organizacionais, incluindo seu código,
    nome, objetivo, datas relevantes, departamento responsável, status e responsável.
    Attributes:
        codigo (CharField): Código único do processo, máximo de 100 caracteres.
        nome (CharField): Nome descritivo do processo, máximo de 255 caracteres.
        objetivo (TextField): Descrição detalhada do objetivo do processo. Opcional.
        data_criacao (DateTimeField): Data e hora em que o processo foi criado no sistema.
            Preenchido automaticamente.
        vigencia (DateTimeField): Data e hora até quando o processo permanece válido. Opcional.
        departamento (ForeignKey): Referência ao departamento responsável pelo processo.
            Pode ser nulo.
        status (CharField): Status atual do processo, com opções pré-definidas:
            - aprovado: Processo aprovado e em vigor.
            - em_revisao: Processo em fase de revisão.
            - em_mapeamento: Processo em fase de mapeamento.
        responsavel (ForeignKey): Referência ao usuário responsável pelo processo.
            Pode ser nulo.
    """

    status_choices = [
        (None, 'Selecione um Status'),
        ('aprovado', 'Aprovado'),
        ('em_revisao', 'Em Revisão'),
        ('em_mapeamento', 'Em Mapeamento'),
        ('obsoleto', 'Obsoleto'),
    ]

    codigo = models.CharField(
        max_length=100, verbose_name='Código', unique=True)
    nome = models.CharField(max_length=255, verbose_name='Nome do Processo')
    objetivo = models.TextField(null=True, blank=True, verbose_name='Objetivo')
    data_criacao = models.DateTimeField(
        auto_now_add=True, verbose_name='Data de Criação')
    vigencia = models.DateTimeField(
        null=True, blank=True, verbose_name='Vigência')
    departamento = models.ForeignKey(
        Departamento,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='processos_departamento',
        verbose_name='Departamento'
    )
    status = models.CharField(
        max_length=20,
        choices=status_choices,
        default='em_revisao',
        verbose_name='Status'
    )

    responsavel = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='processos_responsavel',
        verbose_name='Responsável'
    )

    def __str__(self):
        return self.nome
