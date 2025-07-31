from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from apps.usuarios.views import index

urlpatterns = [
    path('', index, name='index'),  # Página inicial
    path('admin/', admin.site.urls),
    path('usuarios/', include('apps.usuarios.urls')),
]

# Adiciona configuração para servir arquivos de mídia em desenvolvimento
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
