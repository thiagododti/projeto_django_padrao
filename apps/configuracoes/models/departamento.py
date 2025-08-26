from django.db import models
from .empresa import Empresa


class Departamento(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    descricao = models.TextField(blank=True, null=True)
    data_criacao = models.DateField(auto_now_add=True)

    supervisor = models.ManyToManyField(
        'Usuario',
        blank=True,
        related_name='departamentos_supervisionados',
        verbose_name='Supervisores do Departamento'
    )
    empresa = models.ForeignKey(
        Empresa,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='departamentos_por_empresa',
        verbose_name='Empresa do Departamento',
    )
    departamento_pai = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='departamentos_filhos',
        verbose_name='Departamento Pai',
    )

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'Departamento'
        verbose_name_plural = 'Departamentos'
