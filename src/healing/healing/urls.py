from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls), # http://127.0.0.1:8000/admin/4/?next=/admin/
    path('usuarios/', include('usuarios.urls')), # http://127.0.0.1:8000/usuarios/
    path('medicos/', include('medicos.urls')), # http://127.0.0.1:8000/medicos/
    path('pacientes/', include('pacientes.urls')), # http://127.0.0.1:8000/pacientes/
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
