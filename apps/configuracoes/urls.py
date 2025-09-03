from django.urls import path
from .views import *

urlpatterns = [
    # LOGOUT - Registro de Novo Usuário ###############################################
    path('login/', index, name='index'),
    path('logout/', logout_view, name='logout'),
    path('registrar/', registrar, name='registrar'),
    path('construcao/', construcao, name='construcao'),

    # URLS MENU
    path('perfil/', perfil, name='perfil'),
    path('usuarios/', usuario_list_view, name='usuarios'),
    path('departamentos/', departamento_list_view, name='departamentos'),
    path('empresas/', empresa_list_view, name='empresas'),
    path('cargos/', cargo_list_view, name='cargos'),

    # URLS CRUD ########################################################################
    # USUÁRIOS
    path('criar_usuario/', criar_usuario, name='criar_usuario'),
    path('editar_usuario/<int:user_id>/',
         editar_usuario, name='editar_usuario'),

    # DEPARTAMENTOS
    path('criar_departamento/', criar_departamento_view, name='criar_departamento'),
    path('editar_departamento/<int:departamento_id>/',
         editar_departamento_view, name='editar_departamento'),

    # CARGOS
    path('criar_cargo/', criar_cargo_view, name='criar_cargo'),
    path('editar_cargo/<int:cargo_id>/', editar_cargo_view, name='editar_cargo'),

    # EMPRESAS
    path('criar_empresa/', criar_empresa_view, name='criar_empresa'),
    path('editar_empresa/<int:empresa_id>/',
         editar_empresa_view, name='editar_empresa'),


    #####################################################################################

]
