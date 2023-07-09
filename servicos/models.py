from django.db import models
from datetime import datetime
from secrets import token_hex, token_urlsafe
from clientes.models import Cliente


class Servico(models.Model):
    servico = models.CharField(max_length=30)
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True)
    preco = models.DecimalField(max_digits=8, decimal_places=2, null=True)
    data_inicio = models.DateField(null=True)
    data_entrega = models.DateField(null=True)
    descricao = models.CharField(max_length=100, null=True)
    finalizado = models.BooleanField(default=False)
    protocolo = models.CharField(max_length=52, null=True, blank=True)
    identificador = models.CharField(max_length=24, null=True, blank=True)

    def __str__(self) -> str:
        return self.servico

    def save(self, *args, **kwargs):
        if not self.protocolo:
            self.protocolo = datetime.now().strftime("%d/%m/%Y-%H:%M:%S-") + token_hex(16)
        if not self.identificador:
            self.identificador = token_urlsafe(16)
        super(Servico, self).save(*args, **kwargs)