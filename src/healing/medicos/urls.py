from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    #precisa estar logado para acessar essa URL
    path('cadastro_medico/', views.cadastro_medico, name="cadastro_medico"), # http://127.0.0.1:8000/medicos/cadastro_medico/
    path('abrir_horario/', views.abrir_horario, name="abrir_horario"),
    path('consultas_medico/', views.consultas_medico, name="consultas_medico"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)