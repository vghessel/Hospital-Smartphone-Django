from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.shortcuts import redirect, get_object_or_404
from .models import Cliente, Aparelho
import re
import json

def clientes(request):
    if request.method == "GET":
        clientes = Cliente.objects.all()
        return render(request, 'clientes.html', {'clientes': clientes})
    
def novo_cliente(request):
    if request.method == "GET":
        return render(request, 'novo_cliente.html')
    elif request.method == "POST":
        nome_completo = request.POST.get('nome_completo')
        email = request.POST.get('email')
        cpf = request.POST.get('cpf')
        aparelhos = request.POST.getlist('aparelho')
        modelos = request.POST.getlist('modelo')
        codigos = request.POST.getlist('codigo')

        cliente = Cliente.objects.filter(cpf=cpf)

        if cliente.exists():
            return render(request, 'clientes.html', {'nome_completo': nome_completo, 'email': email, 'aparelhos': zip(aparelhos, modelos, codigos) })

        if not re.fullmatch(re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'), email):
            return render(request, 'clientes.html', {'nome_completo': nome_completo,'cpf': cpf, 'aparelhos': zip(aparelhos, modelos, codigos)})

        cliente = Cliente(
            nome_completo = nome_completo,
            email = email,
            cpf = cpf
        )

        cliente.save()

        for aparelho, modelo, codigo in zip(aparelhos, modelos, codigos):
            apa = Aparelho(aparelho=aparelho, modelo=modelo, codigo=codigo, cliente=cliente)
            apa.save()

        return HttpResponse('Cliente salvo com sucesso')
    
def excluir_cliente(request, id):
    try:
        cliente = Cliente.objects.get(id=id)
        cliente.delete()
        return redirect(reverse('clientes'))
    except:
        return redirect(reverse('clientes'))

def att_cliente(request):
    id_cliente = request.POST.get('id_cliente')

    cliente = Cliente.objects.filter(id=id_cliente)
    aparelhos = Aparelho.objects.filter(cliente=cliente[0])

    clientes_json = json.loads(serializers.serialize('json', cliente))[0]['fields'] # str -> json
    cliente_id = json.loads(serializers.serialize('json', cliente))[0]['pk']
    aparelhos_json = json.loads(serializers.serialize('json', aparelhos))
    aparelhos_json = [{'fields': aparelho['fields'], 'id': aparelho['pk']} for aparelho in aparelhos_json]
    data = {'cliente': clientes_json, 'aparelhos': aparelhos_json, 'cliente_id': cliente_id}
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
    
def update_cliente(request, id):
    body = json.loads(request.body)

    nome_completo = body['nome_completo']
    email = body['email']
    cpf = body['cpf']

    cliente = get_object_or_404(Cliente, id=id) # caso não exista o cliente, 404
    try:
        cliente.nome_completo = nome_completo
        cliente.email = email
        cliente.cpf = cpf
        cliente.save()
        return JsonResponse({'status': '200', 'nome_completo': nome_completo,'email': email, 'cpf': cpf})
    except:
        return JsonResponse({'status': '500'})
