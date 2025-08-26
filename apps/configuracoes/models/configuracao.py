from django.db import models


class Configuracao(models.Model):
    nome = models.CharField(max_length=100)
    cnpj = models.CharField(max_length=18, blank=True, null=True)
    logotipo_light = models.ImageField(
        upload_to='logotipos/', null=True, blank=True)
    logotipo_dark = models.ImageField(
        upload_to='logotipos/', null=True, blank=True)
    background_img = models.ImageField(
        upload_to='background/', null=True, blank=True)
    cor_primaria = models.CharField(max_length=7, default="#0c1d41")
    cor_primaria_texto = models.CharField(max_length=7, default="#ffffff")
    cor_primaria_hover = models.CharField(max_length=7, default="#1a3f8d")
    cor_secundaria = models.CharField(max_length=7, default="#ededed")
    cor_background = models.CharField(max_length=7, default="#f9f9fb")
    cor_blocos = models.CharField(max_length=7, default="#ffffff")
    cor_bordas = models.CharField(max_length=7, default="#d1d5db")
    cor_texto = models.CharField(max_length=7, default="#212937")
    cor_texto_hover = models.CharField(max_length=7, default="#1f2937")
    rodape = models.TextField(blank=True)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.nome

    @classmethod
    def configuracao_ativa(cls):
        return cls.objects.filter(ativo=True).first()
