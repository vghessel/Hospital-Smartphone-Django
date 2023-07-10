from django.db import models

class Cliente(models.Model):
    nome_completo = models.CharField(max_length=80, default=True)
    email = models.EmailField(max_length=50)
    cpf = models.CharField(max_length=11)

    def __str__(self) -> str:
        return self.nome
    
class Aparelho(models.Model):
    aparelho = models.CharField(max_length=20)
    modelo = models.CharField(max_length=20)
    codigo = models.IntegerField()
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE) # Deletando o cliente os aparelhos sao deletados tbm
    consertos = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.aparelho