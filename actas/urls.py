"""cabil URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from actas import views

urlpatterns = [
    path('', views.Inicio.as_view(), name="inicio"),
    path('subir/', views.CrearActa.as_view(), name="crear_acta"),
    path('borrar/<str:pk>/', views.BorrarActa, name="borrar_acta"),
    path('actualizar/<str:pk>/', views.UpdateActa.as_view(), name="update_acta"),
    path('enviar/', views.EnviarMail, name="enviar_mail"),
    path('foto/', views.SubirFoto.as_view(), name="subir_foto"),
    path('eliminar/<str:pk>/', views.BorrarFoto, name="borrar_foto"),
]
