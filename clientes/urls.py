from django.urls import path
from . import views

urlpatterns = [
    path('', views.clientes, name="clientes"),
    path('atualiza_cliente/', views.att_cliente, name="atualiza_cliente"),
    path('update_aparelho/<int:id>', views.update_aparelho, name="update_aparelho"),
    path('excluir_aparelho/<int:id>', views.excluir_aparelho, name="excluir_aparelho"),
    path('excluir_cliente/<int:id>', views.excluir_cliente, name="excluir_cliente"),
    path('update_cliente/<int:id>', views.update_cliente, name="update_cliente"),
    path('lista_clientes/', views.lista_clientes, name="lista_clientes")



]