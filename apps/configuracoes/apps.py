from django.apps import AppConfig


class ConfiguracoesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.configuracoes'

    def ready(self):
        import apps.configuracoes.signals
