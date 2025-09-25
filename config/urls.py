from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from apps.configuracoes.views import login_view
from debug_toolbar.toolbar import debug_toolbar_urls
from config import views

urlpatterns = [
    path('',)
    path('', login_view, name='login'),  # Página inicial
    path('admin/', admin.site.urls),
    path('configuracoes/', include('apps.configuracoes.urls')),
    path('organograma/', include('apps.organograma.urls')),
    # rotas de erros
    path('403/', views.erro_403, name='erro_403'),
    path('404/', views.erro_404, name='erro_404'),

]

# Adiciona configuração para servir arquivos de mídia em desenvolvimento
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += debug_toolbar_urls() if settings.DEBUG else []
