from django.db import models


class Cargo(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    descricao = models.TextField(blank=True, null=True)
    nivel_hierarquico = models.IntegerField(default=1)
    data_criacao = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'Cargo'
        verbose_name_plural = 'Cargos'
