from django.urls import path
from . import views

urlpatterns = [
    path('', views.clientes, name="clientes"),
    path('novo_cliente/', views.novo_cliente, name="novo_cliente"),
    path('excluir_cliente/<int:id>', views.excluir_cliente, name="excluir_cliente"),
    path('atualizar_cliente/<int:id>', views.atualizar_cliente, name="atualizar_cliente"),
    path('excluir_aparelho/<int:id>', views.excluir_aparelho, name="excluir_aparelho"),

]