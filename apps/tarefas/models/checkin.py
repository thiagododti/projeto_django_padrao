from django.db import models
from apps.configuracoes.models import Usuario


class Checkin(models.Model):
    usuario = models.ForeignKey(
        Usuario, on_delete=models.CASCADE, related_name='checkins')
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    descricao = models.TextField(blank=True, null=True)
    data_conclusao = models.DateTimeField(blank=True, null=True)
    concluido = models.BooleanField(default=False)

    def __str__(self):
        return f"Checkin de {self.usuario} em {self.data_criacao.strftime('%d/%m/%Y %H:%M')}"

    class Meta:
        ordering = ['-data_criacao']
        verbose_name = 'Checkin'
        verbose_name_plural = 'Checkins'
