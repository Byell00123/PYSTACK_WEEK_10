from django.urls import path
from .import views

urlpatterns = [
    path('cadastro/', views.cadastro, name="cadastro"), # http://127.0.0.1:8000/usuarios/cadastro/
    path('login/', views.login_view, name="login"), # http://127.0.0.1:8000/usuarios/login/
    path('sair/', views.sair, name="sair"), # http://127.0.0.1:8000/usuarios/sair/


]