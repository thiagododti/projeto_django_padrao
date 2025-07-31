from django.contrib.auth import get_user_model
from django.db.models.signals import post_migrate
from django.dispatch import receiver


@receiver(post_migrate)
def criar_superusuario_default(sender, **kwargs):
    Usuario = get_user_model()
    if not Usuario.objects.filter(is_superuser=True).exists():
        Usuario.objects.create_superuser(
            username='admin',
            password='admin123',
            cpf='00000000000',
            cargo='Administrador',
            departamento='TI',
            email='admin@example.com'
        )
