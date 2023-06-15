from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.shortcuts import redirect
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
    aparelhos = Aparelho.objects.filter(cliente=cliente[0])

    clientes_json = json.loads(serializers.serialize('json', cliente))[0]['fields'] # str -> json
    aparelhos_json = json.loads(serializers.serialize('json', aparelhos))
    aparelhos_json = [{'fields': aparelho['fields'], 'id': aparelho['pk']} for aparelho in aparelhos_json]
    data = {'cliente': clientes_json, 'aparelhos': aparelhos_json}
    return JsonResponse(data) # Retornando para o JS

@csrf_exempt
def update_aparelho(request, id):
    nome_aparelho = request.POST.get('aparelho')
    modelo = request.POST.get('modelo')
    codigo = request.POST.get('codigo')

    aparelho = Aparelho.objects.get(id=id)
    list_aparelhos = Aparelho.objects.filter(codigo=codigo).exclude(id=id)
    if list_aparelhos.exists():
        return HttpResponse('Codigo ja existente')
    
    aparelho.aparelho = nome_aparelho
    aparelho.modelo = modelo
    aparelho.codigo = codigo
    aparelho.save()
    return HttpResponse('Dados alterados com sucesso!')

def excluir_aparelho(request, id):
    try:
        aparelho = Aparelho.objects.get(id=id)
        aparelho.delete()
        return redirect(reverse('clientes') + f'?aba=att_cliente&id_cliente={id}')
    except:
        return redirect(reverse('clientes') + f'?aba=att_cliente&id_cliente={id}')