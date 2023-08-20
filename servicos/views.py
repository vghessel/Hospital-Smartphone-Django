from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import FileResponse
from fpdf import FPDF
from io import BytesIO
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
            return redirect(reverse('servicos'))
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
            return redirect(reverse('servicos'))
        else:
            return render(request, 'servico.html', {'form': form, 'identificador': identificador})

def gerar_pdf(request, identificador):
    servico = get_object_or_404(Servico, identificador=identificador)
    
    pdf = FPDF()
    pdf.add_page()

    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, 'HOSPITAL DO SMARTPHONE', 0, 1, 'C')

    pdf.set_font('Arial', 'I', 10)
    pdf.cell(0, 10, 'Telefone: (11)912345678', 0, 1, 'C')
    pdf.cell(0, 10, 'Endereço: Avenida Paulista, 1234', 0, 1, 'C')
    pdf.cell(0, 10, 'CNPJ: 12.345.678/0001-99', 0, 1, 'C')

    pdf.set_font('Arial', 'B', 12)
    pdf.set_fill_color(240, 240, 240)
    pdf.cell(35, 10, 'Cliente:', 1, 0, 'L', 1)
    pdf.cell(0, 10, f'{servico.cliente.nome_completo}', 1, 1, 'L', 1)
    pdf.cell(35, 10, 'Serviço:', 1, 0, 'L', 1)
    pdf.cell(0, 10, f'{servico.servico}', 1, 1, 'L', 1)
    pdf.cell(35, 10, 'Data de Início:', 1, 0, 'L', 1)
    pdf.cell(0, 10, f'{servico.data_inicio}', 1, 1, 'L', 1)
    pdf.cell(35, 10, 'Data de Entrega:', 1, 0, 'L', 1)
    pdf.cell(0, 10, f'{servico.data_entrega}', 1, 1, 'L', 1)
    pdf.cell(35, 10, 'Valor Total:', 1, 0, 'L', 1)
    pdf.cell(0, 10, f'{servico.preco}', 1, 1, 'L', 1)
    pdf.cell(35, 10, 'Protocolo:', 1, 0, 'L', 1)
    pdf.cell(0, 10, f'{servico.protocolo}', 1, 1, 'L', 1)

    pdf_content = pdf.output(dest='S').encode('latin1')
    pdf_bytes = BytesIO(pdf_content)

    return FileResponse(pdf_bytes, as_attachment=True, filename=f"{servico.protocolo}.pdf")

def servicos_filtro(request):
    protocolo = request.GET.get('protocolo')
    servicos = Servico.objects.filter(protocolo__contains=protocolo)
    return render(request, 'listar_servico.html', {'servicos': servicos})
