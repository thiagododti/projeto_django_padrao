from django.urls import path
from .views import *

urlpatterns = [
    path('', relatorio, name='relatorios'),

]
