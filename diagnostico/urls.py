from django.urls import path
from .views import crear_diagnostico

urlpatterns = [
    path('', crear_diagnostico, name='formulario'),
]