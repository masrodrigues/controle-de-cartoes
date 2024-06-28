# urls.py dentro da aplicação cartoes
from django.urls import path
from .views import AdicionarCartaoView, ListaCartoesView, DetalhesCartaoView, RelatorioGastosView, AdicionarGastoView, EditarGastoView, cadastro_categoria

urlpatterns = [
    path('', ListaCartoesView.as_view(), name='lista_cartoes'),
    path('<int:pk>/', DetalhesCartaoView.as_view(), name='detalhes_cartao'),
    path('gastos/adicionar/', AdicionarGastoView.as_view(), name='adicionar_gasto'),
    path('gastos/editar/<int:pk>/', EditarGastoView.as_view(), name='editar_gasto'),
    path('relatorio/gastos/', RelatorioGastosView.as_view(), name='relatorio_gastos'),
    path('cadastro/', cadastro_categoria, name='cadastro_categoria'),  # Corrigido aqui
    path('adicionar/', AdicionarCartaoView.as_view(), name='adicionar_cartao'),
]