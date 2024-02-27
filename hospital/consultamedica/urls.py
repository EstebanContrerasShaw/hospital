from django.urls import path
from .views import *
app_name = 'inventario'
urlpatterns = [
    path('', index , name='index'),
    path('atender/', atender , name='atender'),
    path('liberar/', liberar , name='liberar'),
    path('fumador/', fumadorurgente , name='fumadorurgente'),
    path('masatenciones/', masatendido , name='masatendido'),
    path('anciano/', masanciano , name='masanciano'),
    path('optimizar/', optimizar , name='optimizar'),
    path('paciente/<int:id>', verpaciente , name='verpaciente'),
    path('mayorriesgo/<int:nro>', mayorriesgo , name='mayorriesgo'),
    
]