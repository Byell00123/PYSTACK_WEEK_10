from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls), # http://127.0.0.1:8000/admin/4/?next=/admin/
    path('usuarios/', include('usuarios.urls')), # http://127.0.0.1:8000/usuarios/
    path('medicos/', include('medicos.urls')), # http://127.0.0.1:8000/medicos/
]
