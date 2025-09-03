from django.urls import path
from .views import *

urlpatterns = [
    ######################################## views ajax ##########################################

    path('detalhes_tarefa/<int:tarefa_id>/',
         detalhes_tarefa, name='detalhes_tarefa'),

    # checkin e checkout
    path('deletar_tarefa_checkin/<int:tarefa_id>/',
         deletar_tarefa_checkin, name='deletar_tarefa_checkin'),
    path('remover_conclusao_tarefa_checkin/<int:tarefa_id>/',
         remover_conclusao_tarefa_checkin, name='remover_conclusao_tarefa_checkin'),

    # checkin
    path('checkin/', checkin, name='checkin'),

    path('criar_tarefa/checkin/', criar_tarefa_checkin,
         name='criar_tarefa_checkin'),

    path('editar_tarefa/<int:tarefa_id>/checkin/',
         editar_tarefa_checkin, name='editar_tarefa_checkin'),

    # checkout
    path('checkout/', checkout, name='checkout'),

    path('criar_tarefa/checkout/', criar_tarefa_checkout,
         name='criar_tarefa_checkout'),
    path('editar_tarefa/<int:tarefa_id>/checkout/',
         editar_tarefa_checkout, name='editar_tarefa_checkout'),
    path('concluir_tarefa/<int:tarefa_id>/checkout/',
         concluir_tarefa_checkout, name='concluir_tarefa_checkout'),
    path('encerrar_checkout/', encerrar_checkout, name='encerrar_checkout'),

]
