from django.contrib.auth.models import AbstractUser
from django.db import models
import os
from django.utils.deconstruct import deconstructible


@deconstructible
class UsuarioPathAndRename:
    def __call__(self, instance, filename):
        ext = os.path.splitext(filename)[1]  # extensão do arquivo
        filename = f"{instance.username}{ext}"  # novo nome
        return os.path.join('profile_photos', filename)  # caminho final


class Usuario(AbstractUser):
    cpf = models.CharField(max_length=11, unique=True)
    cargo = models.ForeignKey(
        'Cargo', on_delete=models.SET_NULL, null=True, blank=True)
    departamento = models.ManyToManyField(
        'Departamento',
        blank=True,
        related_name='usuarios_membros',
        verbose_name='Departamentos que o usuário participa'
    )
    is_staff = models.BooleanField(default=False, verbose_name="É Staff?")
    photo = models.ImageField(upload_to=UsuarioPathAndRename(),
                              blank=True, null=True, verbose_name="Foto do Usuário")
    data_nascimento = models.DateField(
        blank=True, null=True, verbose_name="Data de Nascimento")
    data_contratacao = models.DateField(
        blank=True, null=True, verbose_name="Data de Contratação")
