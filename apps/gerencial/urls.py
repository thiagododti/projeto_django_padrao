from django.urls import path
from .views import *

urlpatterns = [
    path('', gerencial, name='gerencial'),
    path('indicadores/', indicadores, name='indicadores'),
    path('funcionario/<int:id>/', dados_funcionario, name='dados_funcionario'),

]
