# yourapp/signals.py
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.db.models.signals import m2m_changed

from .models import Configuracao, Departamento, Usuario

# Criação de configuração padrão


@receiver(post_migrate)
def criar_Configuracao_default(sender, **kwargs):
    if not Configuracao.objects.exists():
        Configuracao.objects.create(
            nome='Empresa Padrão',
            cnpj='00.000.000/0000-00',
            cor_primaria='#1c191a',
            cor_primaria_texto='#ffffff',
            cor_primaria_hover='#1a3f8d',
            cor_secundaria='#1c191a',
            cor_background='#f9f9fb',
            cor_blocos='#ffffff',
            cor_bordas='#d1d5db',
            cor_texto='#000000',
            cor_texto_hover='#1f2937',
            rodape='Rodapé padrão',
            ativo=True
        )

# Criação de superusuário padrão


@receiver(post_migrate)
def criar_superusuario_default(sender, **kwargs):
    Usuario = get_user_model()
    if not Usuario.objects.filter(is_superuser=True).exists():
        Usuario.objects.create_superuser(
            username='admin',
            password='admin123',
            cpf='00000000000',
            email='admin@example.com'
        )

# Adicionar supervisores como membros do departamento


@receiver(m2m_changed, sender=Departamento.supervisor.through)
def adicionar_supervisor_como_membro(sender, instance, action, pk_set, **kwargs):
    if action == 'post_add':  # quando novos supervisores forem adicionados
        for usuario_id in pk_set:
            usuario = Usuario.objects.get(pk=usuario_id)
            usuario.departamento.add(instance)
