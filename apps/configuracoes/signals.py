# yourapp/signals.py
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Empresa


@receiver(post_migrate)
def criar_empresa_default(sender, **kwargs):
    if not Empresa.objects.exists():
        Empresa.objects.create(
            nome='Empresa Padrão',
            cnpj='00.000.000/0000-00',
            cor_primaria='#2c3c9c',
            cor_primaria_texto='#ffffff',
            cor_primaria_hover='#364cd6',
            cor_secundaria='#4b5563',
            cor_background='#f9fafb',
            cor_blocos='#e5e7eb',
            cor_bordas='#d1d5db',
            cor_texto='#212937',
            rodape='Rodapé padrão',
            ativo=True
        )
