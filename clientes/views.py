from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from .models import Cliente, Aparelho
import re
import json

def clientes(request):
    if request.method == "GET":
        clientes_list = Cliente.objects.all()
        return render(request, 'clientes.html', {'clientes': clientes_list})
    elif request.method == "POST":
        nome = request.POST.get('nome')
        sobrenome = request.POST.get('sobrenome')
        email = request.POST.get('email')
        cpf = request.POST.get('cpf')
        aparelhos = request.POST.getlist('aparelho')
        modelos = request.POST.getlist('modelo')
        codigos = request.POST.getlist('codigo')

        cliente = Cliente.objects.filter(cpf=cpf)

        if cliente.exists():
            return render(request, 'clientes.html', {'nome': nome, 'sobrenome': sobrenome, 'email': email, 'aparelhos': zip(aparelhos, modelos, codigos) })

        if not re.fullmatch(re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'), email):
            return render(request, 'clientes.html', {'nome': nome, 'sobrenome': sobrenome, 'cpf': cpf, 'aparelhos': zip(aparelhos, modelos, codigos)})

        cliente = Cliente(
            nome = nome,
            sobrenome = sobrenome,
            email = email,
            cpf = cpf
        )

        cliente.save()

        for aparelho, modelo, codigo in zip(aparelhos, modelos, codigos):
            apa = Aparelho(aparelho=aparelho, modelo=modelo, codigo=codigo, cliente=cliente)
            apa.save()

        return HttpResponse('Teste')

def att_cliente(request):
    id_cliente = request.POST.get('id_cliente')
    cliente = Cliente.objects.filter(id=id_cliente)
    cliente_json = json.loads(serializers.serialize('json', cliente))[0]['fields'] # str -> json
    return JsonResponse(cliente_json) # Retornando para o JS
