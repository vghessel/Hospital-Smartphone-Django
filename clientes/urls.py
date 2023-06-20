from django.urls import path
from . import views

urlpatterns = [
    path('', views.clientes, name="clientes"),
    path('atualiza_cliente/', views.att_cliente, name="atualiza_cliente"),
    path('update_aparelho/<int:id>', views.update_aparelho, name="update_aparelho"),
    path('excluir_aparelho/<int:id>', views.excluir_aparelho, name="excluir_aparelho"),
    path('update_cliente/<int:id>', views.update_cliente, name="update_cliente")



]