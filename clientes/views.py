from django.shortcuts import render
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

        return redirect(reverse('clientes'))
    
def excluir_cliente(request, id):
    try:
        cliente = Cliente.objects.get(id=id)
        cliente.delete()
        return redirect(reverse('clientes'))
    except:
        return redirect(reverse('clientes'))

def atualizar_cliente(request, id):

    # Trazer info do banco para o front
    if request.method == "GET":
        cliente = Cliente.objects.filter(id=id)
        aparelhos = Aparelho.objects.filter(cliente=cliente[0])
        cliente_json = json.loads(serializers.serialize('json', cliente))[0]['fields']
        nome_completo = cliente_json['nome_completo']
        email = cliente_json['email']
        cpf = cliente_json['cpf']
        return render(request, 'atualizar_cliente.html', {'id': id, 'nome_completo': nome_completo, 'email': email, 'cpf': cpf, 'aparelhos': aparelhos})
    
    # Salvar novos dados no banco
    elif request.method == "POST":
        nome_completo = request.POST.get('nome_completo')
        email = request.POST.get('email')
        cpf = request.POST.get('cpf')
        aparelhos = request.POST.getlist('aparelho')
        modelos = request.POST.getlist('modelo')
        codigos = request.POST.getlist('codigo')

        if not re.fullmatch(re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'), email):
            return render(request, 'clientes.html')
        
        cliente = get_object_or_404(Cliente, id=id)

        cliente.nome_completo = nome_completo
        cliente.email = email
        cliente.cpf = cpf

        cliente.save()

        for aparelho, modelo, codigo in zip(aparelhos, modelos, codigos):
            apa = Aparelho.objects.get(codigo=codigo)
            apa.aparelho = aparelho
            apa.modelo = modelo
            apa.codigo = codigo
            apa.save()

        return redirect(reverse('clientes'))


def excluir_aparelho(request, id):
    try:
        aparelho = Aparelho.objects.get(id=id)
        aparelho.delete()
        return redirect(reverse('clientes'))
    except:
        return redirect(reverse('clientes'))

