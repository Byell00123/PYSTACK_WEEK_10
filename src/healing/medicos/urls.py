from django.urls import path
from . import views

urlpatterns = [
    #precisa estar logado para acessar essa URL
    path('cadastro_medico/', views.cadastro_medico, name="cadastro_medico"), # http://127.0.0.1:8000/medicos/cadastro_medico/
]