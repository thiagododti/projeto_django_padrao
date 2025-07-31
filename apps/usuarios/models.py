from django.contrib.auth.models import AbstractUser
from django.db import models
import os


class Usuario(AbstractUser):
    cpf = models.CharField(max_length=11, unique=True)
    cargo = models.CharField(max_length=100)
    departamento = models.CharField(max_length=100)

    photo = models.ImageField(upload_to="profile_photos/",blank=True, null=True, verbose_name="Foto do Usuário")
    data_nascimento: models.DateField = models.DateField(blank=True, null=True, verbose_name="Data de Nascimento")
    data_contratacao: models.DateField = models.DateField(blank=True, null=True, verbose_name="Data de Contratação")

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        if self.photo:
            # Extrai a extensão do arquivo original
            ext = os.path.splitext(self.photo.name)[1]
            # Renomeia o arquivo da foto para o nome do usuário
            self.photo.name = f'{self.username}{ext}'
        super(Usuario, self).save(*args, **kwargs)

    def __str__(self):
        return self.get_full_name() or self.username
