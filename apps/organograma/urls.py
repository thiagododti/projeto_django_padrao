from django.urls import path
from .views import *

urlpatterns = [
    path('', organograma, name='organograma'),
    path('json/', organograma_json, name='organograma_json'),
    path('membros/<int:departamento_id>/',
         departamento_membros_supervisores, name='membros'),
]
