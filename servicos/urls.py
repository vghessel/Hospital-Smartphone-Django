from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_servico, name="servicos"),
    path('novo_servico/', views.novo_servico, name="novo_servico"),
    path('servico/<str:identificador>/', views.servico, name="servico"),
]