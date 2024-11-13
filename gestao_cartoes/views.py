import logging
from datetime import date, timedelta
from calendar import monthrange

from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView

from .forms import GastoForm, CartaoForm, CategoriaForm, ConfirmDeleteForm
from .models import Cartao, Gasto, Categoria

logger = logging.getLogger(__name__)

from django.views.generic import CreateView
from .forms import CartaoForm
from .models import Cartao

class AdicionarCartaoView(CreateView):
    model = Cartao
    form_class = CartaoForm
    template_name = 'adicionar_cartao.html'
    success_url = reverse_lazy('lista_cartoes')

def calcular_periodo_vencimento(mes_atual, ano_atual, dia_vencimento):
    """
    Calcula o intervalo de datas com base no vencimento do cartão.
    """
    try:
        data_vencimento_atual = date(ano_atual, mes_atual, dia_vencimento)
    except ValueError:
        # Caso o dia do vencimento ultrapasse o último dia do mês
        ultimo_dia_mes = monthrange(ano_atual, mes_atual)[1]
        data_vencimento_atual = date(ano_atual, mes_atual, ultimo_dia_mes)

    if mes_atual == 1:
        mes_anterior = 12
        ano_anterior = ano_atual - 1
    else:
        mes_anterior = mes_atual - 1
        ano_anterior = ano_atual

    ultimo_dia_mes_anterior = monthrange(ano_anterior, mes_anterior)[1]
    data_inicio = date(ano_anterior, mes_anterior, min(dia_vencimento + 1, ultimo_dia_mes_anterior))

    return data_inicio, data_vencimento_atual

class ListaCartoesView(LoginRequiredMixin, ListView):
    model = Cartao
    template_name = 'lista_cartoes.html'
    context_object_name = 'cartoes'

from datetime import date, timedelta
from django.views.generic import DetailView
from .models import Cartao, Gasto


class DetalhesCartaoView(DetailView):
    model = Cartao
    template_name = 'detalhes_cartao.html'
    context_object_name = 'cartao'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cartao = self.object

        mes_param = self.request.GET.get('mes', None)
        ano_atual = date.today().year
        mes_atual = date.today().month

        if mes_param and mes_param.isdigit():
            mes_atual = int(mes_param)

        dia_vencimento = cartao.vencimento
        data_inicio, data_fim = calcular_periodo_vencimento(mes_atual, ano_atual, dia_vencimento)

        gastos = Gasto.objects.filter(cartao=cartao, data__gte=data_inicio, data__lt=data_fim)
        total_gastos = gastos.aggregate(Sum('valor'))['valor__sum'] or 0

        context.update({
            'gastos': gastos,
            'total_gastos': total_gastos,
            'mes_atual': mes_atual,
            'ano_atual': ano_atual,
            'mes_anterior': mes_atual - 1 if mes_atual > 1 else 12,
            'mes_proximo': mes_atual + 1 if mes_atual < 12 else 1,
            'ano_anterior': ano_atual - 1 if mes_atual == 1 else ano_atual,
            'ano_proximo': ano_atual + 1 if mes_atual == 12 else ano_atual,
        })
        return context

class RelatorioGastosView(TemplateView):
    template_name = 'relatorio_gastos.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mes_param = self.request.GET.get('mes', None)
        ano_atual = timezone.now().year
        mes_atual = timezone.now().month

        if mes_param and mes_param.isdigit():
            mes_atual = int(mes_param)

        context.update({
            'mes_selecionado': mes_atual,
            'nome_mes_selecionado': self.mapear_numero_para_mes(mes_atual),
            'meses': [(i, self.mapear_numero_para_mes(i)) for i in range(1, 13)],
        })

        relatorio = []
        total_gastos_geral = 0
        cartoes = Cartao.objects.all()

        for cartao in cartoes:
            dia_vencimento = cartao.vencimento
            data_inicio, data_fim = calcular_periodo_vencimento(mes_atual, ano_atual, dia_vencimento)

            gastos = Gasto.objects.filter(cartao=cartao, data__gte=data_inicio, data__lt=data_fim)
            total_gastos = gastos.aggregate(Sum('valor'))['valor__sum'] or 0

            if total_gastos > 0:
                relatorio.append({'cartao': cartao, 'total_gastos': total_gastos})
                total_gastos_geral += total_gastos

        context.update({
            'relatorio': relatorio,
            'total_gastos_geral': total_gastos_geral,
        })
        return context

    @staticmethod
    def mapear_numero_para_mes(numero_mes):
        meses = {
            1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril",
            5: "Maio", 6: "Junho", 7: "Julho", 8: "Agosto",
            9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro"
        }
        return meses.get(numero_mes, "Mês Inválido")

class AdicionarGastoView(CreateView):
    model = Gasto
    form_class = GastoForm
    template_name = 'adicionar_gasto.html'
    success_url = reverse_lazy('lista_cartoes')

    def form_valid(self, form):
        with transaction.atomic():
            self.object = form.save(commit=False)
            parcelas = form.cleaned_data.get('parcelas', 1)
            self.object.save()

            for i in range(1, parcelas):
                Gasto.objects.create(
                    cartao=self.object.cartao,
                    valor=self.object.valor,
                    data=self.object.data + timedelta(days=30 * i),
                    categoria=self.object.categoria,
                    descricao=f"{self.object.descricao} (Parcela {i + 1} de {parcelas})",
                    parcelas=1
                )
        return super().form_valid(form)
from django.shortcuts import render, get_object_or_404, redirect
from .models import Cartao
from .forms import CartaoForm

@login_required
def editar_cartao(request, pk):
    cartao = get_object_or_404(Cartao, pk=pk)
    if request.method == 'POST':
        form = CartaoForm(request.POST, request.FILES, instance=cartao)
        if form.is_valid():
            form.save()
            return redirect('lista_cartoes')  # Redireciona para a lista de cartões após editar.
    else:
        form = CartaoForm(instance=cartao)
    return render(request, 'editar_cartao.html', {'form': form, 'cartao': cartao})

class EditarGastoView(UpdateView):
    model = Gasto
    form_class = GastoForm
    template_name = 'editar_gasto.html'
    success_url = reverse_lazy('lista_cartoes')

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Gasto, Cartao

from django.urls import reverse

@login_required
def excluir_gasto(request, gasto_id):
    gasto = get_object_or_404(Gasto, id=gasto_id)
    cartao = gasto.cartao
    gasto.delete()

    # Redireciona de volta para a página de detalhes do cartão
    return redirect(reverse('detalhes_cartao', args=[cartao.id]))



@login_required
def excluir_cartao(request, pk):
    cartao = get_object_or_404(Cartao, pk=pk)
    if request.method == 'POST':
        cartao.delete()
        return redirect('lista_cartoes')  # Certifique-se de que 'lista_cartoes' é o nome correto da sua view.
    return render(request, 'confirmar_exclusao.html', {'cartao': cartao})


import logging
logger = logging.getLogger(__name__)


@login_required
def gastos_do_cartao(request, cartao_id):
    cartao = get_object_or_404(Cartao, id=cartao_id)
    gastos = Gasto.objects.filter(cartao=cartao).values('id', 'descricao', 'valor', 'data')  # Certifique-se de incluir o 'id'

    return JsonResponse({'gastos': list(gastos)})




def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
            return redirect('lista_cartoes')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})
from django.shortcuts import render, redirect
from .forms import CategoriaForm
from .models import Categoria

@login_required
def cadastro_categoria(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('cadastro_categoria')
    else:
        form = CategoriaForm()
    categorias = Categoria.objects.all()
    return render(request, 'cadastro_categoria.html', {'form': form, 'categorias': categorias})
