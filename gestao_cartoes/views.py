from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView
from django.db.models import Sum, Q
from django.utils import timezone
from datetime import datetime

from .models import Cartao, Gasto
from .forms import GastoForm, CategoriaForm

import logging

logger = logging.getLogger(__name__)

class ListaCartoesView(ListView):
    model = Cartao
    template_name = 'lista_cartoes.html'
    context_object_name = 'cartoes'

class DetalhesCartaoView(DetailView):
    model = Cartao
    template_name = 'detalhes_cartao.html'
    context_object_name = 'cartao'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        logger.debug(f"Vencimento: {self.object.vencimento}")
        context['gastos'] = Gasto.objects.filter(cartao=self.get_object()).order_by('-data')
        return context

from django.db import transaction
from datetime import timedelta

from django.views.generic.edit import CreateView
from django.db import transaction
from datetime import timedelta
from .models import Gasto  # Certifique-se de que o caminho de importação está correto

class AdicionarGastoView(CreateView):
    model = Gasto
    fields = ['cartao', 'valor', 'data', 'categoria', 'descricao', 'parcelas']
    template_name = 'adicionar_gasto.html'  # Substitua pelo caminho correto do seu template
    success_url = '/url-de-sucesso/'  # Substitua pela URL para redirecionar após o sucesso

    def form_valid(self, form):
        with transaction.atomic():  # Garante que todas as inserções sejam feitas juntas
            self.object = form.save(commit=False)
            parcelas = form.cleaned_data.get('parcelas', 1)
            self.object.save()  # Salva o primeiro gasto
            for i in range(1, parcelas):
                gasto_parcelado = Gasto(
                    cartao=self.object.cartao,
                    valor=self.object.valor,
                    data=self.object.data + timedelta(days=30*i),  # Ajusta a data para o próximo mês
                    categoria=self.object.categoria,
                    descricao=f"{self.object.descricao} (Parcela {i+1} de {parcelas})",
                    parcelas=1  # Cada parcela é tratada individualmente
                )
                gasto_parcelado.save()
        return super().form_valid(form)

class EditarGastoView(UpdateView):
    model = Gasto
    form_class = GastoForm
    template_name = 'editar_gasto.html'
    success_url = reverse_lazy('lista_cartoes')

import logging

# Configura o logger para o Django
logger = logging.getLogger(__name__)

from django.views.generic import TemplateView
from django.utils import timezone

from django.views.generic import TemplateView
from django.utils import timezone
from django.db.models import Sum
from datetime import datetime

from .models import Gasto, Cartao

class RelatorioGastosView(TemplateView):
    template_name = 'relatorio_gastos.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mes_param = self.request.GET.get('mes', None)
        ano_atual = timezone.now().year
        mes_atual = timezone.now().month
        if mes_param and mes_param.isdigit():
            mes_num = int(mes_param)
            if 1 <= mes_num <= 12:
                mes_atual = mes_num
        context['mes_selecionado'] = mes_atual
        context['nome_mes_selecionado'] = self.mapear_numero_para_mes(mes_atual)
        context['meses'] = [(i, self.mapear_numero_para_mes(i)) for i in range(1, 13)]

        # Filtrar gastos por mês
        primeiro_dia_mes = datetime(ano_atual, mes_atual, 1)
        ultimo_dia_mes = datetime(ano_atual, mes_atual + 1, 1) if mes_atual < 12 else datetime(ano_atual + 1, 1, 1)
        gastos_mes = Gasto.objects.filter(data__gte=primeiro_dia_mes, data__lt=ultimo_dia_mes).order_by('cartao')
        relatorio = {}
        for gasto in gastos_mes:
            if gasto.cartao not in relatorio:
                relatorio[gasto.cartao] = 0
            relatorio[gasto.cartao] += gasto.valor
        context['relatorio'] = [{'cartao': cartao, 'total_gastos': total} for cartao, total in relatorio.items()]

        return context

    def mapear_numero_para_mes(self, numero_mes):
        meses = {
            1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril",
            5: "Maio", 6: "Junho", 7: "Julho", 8: "Agosto",
            9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro"
        }
        return meses.get(numero_mes, "Mês Inválido")

class AdicionarCartaoView(CreateView):
    model = Cartao
    fields = ['nome', 'limite', 'vencimento']
    template_name = 'adicionar_cartao.html'
    success_url = reverse_lazy('lista_cartoes')

def gastos_por_categoria(request, categoria_id):
    gastos = Gasto.objects.filter(categoria__id=categoria_id)
    return render(request, 'gastos_por_categoria.html', {'gastos': gastos})

def cadastro_categoria(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_cartoes')
    else:
        form = CategoriaForm()
    return render(request, 'cadastro_categoria.html', {'form': form})

