from django.db import models
from apps.configuracoes.models import Empresa, Departamento
from .checkin import Checkin
from datetime import timedelta

# Create your models here.


class Tarefa(models.Model):
    checkin = models.ForeignKey(
        Checkin, on_delete=models.CASCADE, related_name='tarefas')
    tipo = models.CharField(
        max_length=20, choices=[('planejada', 'Planejada'), ('nao_planejada', 'Não Planejada'), ('reuniao', 'Reunião')], default='planejada')
    titulo = models.CharField(blank=True, null=True, max_length=200)
    descricao = models.TextField(blank=True, null=True)
    observacoes = models.TextField(blank=True, null=True)
    horas_estimadas = models.DurationField(
        default=timedelta(hours=0, minutes=0, seconds=0))
    prioridade = models.CharField(
        max_length=10, choices=[('Baixa', 'Baixa'), ('Média', 'Média'), ('Alta', 'Alta')], default='Média')

    concluida = models.BooleanField(default=False)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_conclusao = models.DateTimeField(blank=True, null=True)
    data_inicio_real = models.DateTimeField(blank=True, null=True)
    data_conclusao_real = models.DateTimeField(blank=True, null=True)
    origem_tarefa = models.ForeignKey(
        Empresa,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tarefas_origem'
    )
    destino_tarefa = models.ForeignKey(
        Empresa,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tarefas_destino'
    )
    cliente_tarefa = models.CharField(blank=True, null=True, max_length=200)
    solicitacao_diretoria = models.BooleanField(default=False)
    tarefa_departamento = models.ForeignKey(
        Departamento,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tarefas_departamento'
    )

    def __str__(self):
        return f"Tarefa: {self.titulo[:30]}{'...' if len(self.titulo) > 30 else ''}"

    class Meta:
        ordering = ['data_criacao']
        verbose_name = 'Tarefa de Checkin'
        verbose_name_plural = 'Tarefas de Checkin'
