from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .forms import FormServico
from .models import Servico


def novo_servico(request):
    if request.method == "GET":
        form = FormServico()
        return render(request, 'novo_servico.html', {'form': form })
    elif request.method == "POST":
        form = FormServico(request.POST)

        if form.is_valid():
            form.save()
            return HttpResponse('Salvo com sucesso')
        else:
            return render(request, 'novo_servico.html', {'form': form}) # Enviar o form preenchido para manter as infos caso o save de errado
        
def listar_servico(request):
    if request.method == "GET":
        servicos = Servico.objects.all()
        return render(request, 'listar_servico.html', {'servicos': servicos})
    
def servico(request, identificador):
    servico = get_object_or_404(Servico, identificador=identificador)
    form = FormServico(instance=servico)
    return render(request, 'servico.html', {'form': form, 'identificador': identificador})

def atualizar_servico(request, identificador):
    servico = get_object_or_404(Servico, identificador=identificador)
    form = FormServico(instance=servico)

    if(request.method == 'POST'):
        form = FormServico(request.POST, instance=servico)

        if(form.is_valid()):
            servico = form.save(commit=False)
            servico.servico = form.cleaned_data['servico']
            servico.cliente = form.cleaned_data['cliente']
            servico.preco = form.cleaned_data['preco']
            servico.data_inicio = form.cleaned_data['data_inicio']
            servico.data_entrega = form.cleaned_data['data_entrega']
            servico.descricao = form.cleaned_data['descricao']
            servico.finalizado = form.cleaned_data['finalizado']
            servico.protocolo = form.cleaned_data['protocolo']
            servico.save()
            return HttpResponse('Salvo com sucesso')
        else:
            return render(request, 'servico.html', {'form': form, 'identificador': identificador})   