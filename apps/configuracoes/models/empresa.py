from django.db import models


class Empresa(models.Model):
    nome = models.CharField(max_length=200, verbose_name="Nome da Empresa")
    cnpj = models.CharField(max_length=14, unique=True, verbose_name="CNPJ")
    razao_social = models.CharField(
        max_length=255, verbose_name="Razão Social")
    endereco = models.CharField(
        max_length=255, verbose_name="Endereço", blank=True, null=True)
    telefone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    data_fundacao = models.DateField(
        verbose_name="Data de Fundação", blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    logo = models.ImageField(
        upload_to="empresas_logos/", blank=True, null=True)
    data_cadastro = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True, verbose_name="Ativo")
    cor_empresa = models.CharField(
        max_length=7, default="#2c3e50", verbose_name="Cor da Empresa")

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'Empresa'
        verbose_name_plural = 'Empresas'
