from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView
from django.views.generic.edit import DeleteView
from django.utils import timezone
from django.db import transaction
from django.db.models import Sum, Q
from datetime import datetime, date, timedelta
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Cartao, Gasto
from .forms import GastoForm, CartaoForm, CategoriaForm, ConfirmDeleteForm

import logging

# Configura o logger para o Django
logger = logging.getLogger(__name__)
from django.contrib.auth.mixins import LoginRequiredMixin

class ListaCartoesView(LoginRequiredMixin, ListView):
    model = Cartao
    template_name = 'lista_cartoes.html'
    context_object_name = 'cartoes'


# Detalhes do Cartão
from datetime import date, timedelta
from django.views.generic.detail import DetailView
from .models import Cartao, Gasto

class DetalhesCartaoView(DetailView):
    model = Cartao
    template_name = 'detalhes_cartao.html'
    context_object_name = 'cartao'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cartao = self.object

        hoje = date.today()
        vencimento_dia = cartao.vencimento

        # Calcula o próximo vencimento
        if hoje.day > vencimento_dia:
            mes_vencimento = hoje.month + 1 if hoje.month < 12 else 1
            ano_vencimento = hoje.year if hoje.month < 12 else hoje.year + 1
        else:
            mes_vencimento = hoje.month
            ano_vencimento = hoje.year

        proximo_vencimento = date(ano_vencimento, mes_vencimento, vencimento_dia)

        # Ajusta a data de fechamento para ser 10 dias antes do próximo vencimento
        data_fim = proximo_vencimento - timedelta(days=10)

        # Calcula a data de início como 30 dias antes da data de fim
        data_inicio = data_fim - timedelta(days=30)

        gastos = Gasto.objects.filter(cartao=cartao, data__gte=data_inicio, data__lt=data_fim)
        total_gastos = gastos.aggregate(Sum('valor'))['valor__sum'] or 0

        context['data_fechamento'] = data_fim
        context['total_gastos'] = total_gastos
        context['gastos'] = gastos
        return context

# Adicionar Gasto
class AdicionarGastoView(CreateView):
    model = Gasto
    form_class = GastoForm
    template_name = 'adicionar_gasto.html'
    success_url = reverse_lazy('lista_cartoes')

    def form_valid(self, form):
        with transaction.atomic():
            self.object = form.save(commit=False)
            parcelas = form.cleaned_data.get('parcelas', 1)
            self.object.save()  # Salva o primeiro gasto
            for i in range(1, parcelas):
                gasto_parcelado = Gasto(
                    cartao=self.object.cartao,
                    valor=self.object.valor,
                    data=self.object.data + timedelta(days=30 * i),
                    categoria=self.object.categoria,
                    descricao=f"{self.object.descricao} (Parcela {i + 1} de {parcelas})",
                    parcelas=1
                )
                gasto_parcelado.save()
        return super().form_valid(form)

# Editar Gasto
class EditarGastoView(UpdateView):
    model = Gasto
    form_class = GastoForm
    template_name = 'editar_gasto.html'
    success_url = reverse_lazy('lista_cartoes')

from django.views.generic import TemplateView
from django.utils import timezone
from django.db.models import Sum
from datetime import date, timedelta
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

        # Filtrar gastos por mês usando o período de fechamento
        relatorio = []
        total_gastos_geral = 0
        cartoes = Cartao.objects.all()

        for cartao in cartoes:
            # Definindo o próximo vencimento para o mês atual selecionado
            mes_vencimento = mes_atual if mes_atual >= date.today().month else mes_atual + 1
            ano_vencimento = ano_atual if mes_vencimento >= date.today().month else ano_atual + 1
            proximo_vencimento = date(ano_vencimento, mes_vencimento, cartao.vencimento)

            # Ajusta a data de fechamento para ser 10 dias antes do próximo vencimento
            data_fim = proximo_vencimento - timedelta(days=10)
            data_inicio = data_fim - timedelta(days=30)

            # Filtra os gastos do cartão usando o período de fechamento
            gastos = Gasto.objects.filter(cartao=cartao, data__gte=data_inicio, data__lt=data_fim)
            total_gastos = gastos.aggregate(Sum('valor'))['valor__sum'] or 0

            if total_gastos > 0:
                relatorio.append({'cartao': cartao, 'total_gastos': total_gastos})
                total_gastos_geral += total_gastos

        context['relatorio'] = relatorio
        context['total_gastos_geral'] = total_gastos_geral

        return context

    def mapear_numero_para_mes(self, numero_mes):
        meses = {
            1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril",
            5: "Maio", 6: "Junho", 7: "Julho", 8: "Agosto",
            9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro"
        }
        return meses.get(numero_mes, "Mês Inválido")





# Adicionar Cartão
class AdicionarCartaoView(CreateView):
    model = Cartao
    form_class = CartaoForm
    template_name = 'adicionar_cartao.html'
    success_url = reverse_lazy('lista_cartoes')

    def get_form_kwargs(self):
        """Este método é sobrescrito para incluir request.FILES no formulário."""
        kwargs = super().get_form_kwargs()
        if self.request.method in ('POST', 'PUT'):
            kwargs['files'] = self.request.FILES
        return kwargs

# Editar Cartão
def editar_cartao(request, cartao_id):
    cartao = get_object_or_404(Cartao, id=cartao_id)
    if request.method == 'POST':
        form = CartaoForm(request.POST, instance=cartao)
        if form.is_valid():
            form.save()
            return redirect('lista_cartoes')
    else:
        form = CartaoForm(instance=cartao)
    return render(request, 'editar_cartao.html', {'form': form})

# Excluir Cartão
def excluir_cartao_view(request, pk):
    cartao = get_object_or_404(Cartao, pk=pk)
    if request.method == 'POST':
        form = ConfirmDeleteForm(request.POST)
        if form.is_valid() and form.cleaned_data['confirm']:
            cartao.delete()
            return redirect(reverse('lista_cartoes'))
    else:
        form = ConfirmDeleteForm()
    return render(request, 'confirmar_exclusao.html', {'form': form, 'cartao': cartao})

# Excluir Gasto
def excluir_gasto(request, gasto_id):
    gasto = get_object_or_404(Gasto, id=gasto_id)
    cartao_id = gasto.cartao.id
    gasto.delete()
    return redirect('detalhes_cartao', pk=cartao_id)

# Gastos por Categoria
def gastos_por_categoria(request, categoria_id):
    gastos = Gasto.objects.filter(categoria__id=categoria_id)
    return render(request, 'gastos_por_categoria.html', {'gastos': gastos})

# Cadastro de Categoria
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView
from django.views.generic.edit import DeleteView
from django.utils import timezone
from django.db import transaction
from django.db.models import Sum, Q
from datetime import datetime, date, timedelta
from .models import Cartao, Gasto, Categoria
from .forms import GastoForm, CartaoForm, CategoriaForm, ConfirmDeleteForm

# Cadastro de Categoria
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

# Editar Categoria
def editar_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            return redirect('cadastro_categoria')
    else:
        form = CategoriaForm(instance=categoria)
    return render(request, 'editar_categoria.html', {'form': form, 'categorias': categoria})

# Excluir Categoria
def excluir_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)
    if request.method == 'POST':
        categoria.delete()
        return redirect('cadastro_categoria')
    return render(request, 'confirmar_exclusao_categoria.html', {'categorias': categoria})

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('lista_cartoes')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

# gestao_cartoes/views.py
from django.shortcuts import redirect
from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    return redirect('login')

# views.py

from django.http import JsonResponse

@login_required
def gastos_do_cartao(request, cartao_id):
    try:
        cartao = Cartao.objects.get(id=cartao_id)
    except Cartao.DoesNotExist:
        return JsonResponse({'error': 'Cartão não encontrado'}, status=404)

    mes_param = request.GET.get('mes', None)
    ano_atual = timezone.now().year
    mes_atual = timezone.now().month
    if mes_param and mes_param.isdigit():
        mes_num = int(mes_param)
        if 1 <= mes_num <= 12:
            mes_atual = mes_num

    # Definindo o próximo vencimento para o mês atual selecionado
    mes_vencimento = mes_atual if mes_atual >= date.today().month else mes_atual + 1
    ano_vencimento = ano_atual if mes_vencimento >= date.today().month else ano_atual + 1
    proximo_vencimento = date(ano_vencimento, mes_vencimento, cartao.vencimento)

    # Ajusta a data de fechamento para ser 10 dias antes do próximo vencimento
    data_fim = proximo_vencimento - timedelta(days=10)
    data_inicio = data_fim - timedelta(days=30)

    # Filtra os gastos do cartão usando o período de fechamento
    gastos = Gasto.objects.filter(cartao=cartao, data__gte=data_inicio, data__lt=data_fim)

    gastos_data = list(gastos.values('descricao', 'valor', 'data'))
    return JsonResponse({'gastos': gastos_data})
