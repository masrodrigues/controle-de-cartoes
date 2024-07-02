# urls.py dentro da aplicação cartoes
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import AdicionarCartaoView, ListaCartoesView, DetalhesCartaoView, RelatorioGastosView, AdicionarGastoView, EditarGastoView, cadastro_categoria
from django.urls import path
from .views import editar_cartao, excluir_cartao_view
from . import views
urlpatterns = [
    path('', ListaCartoesView.as_view(), name='lista_cartoes'),
    path('<int:pk>/', DetalhesCartaoView.as_view(), name='detalhes_cartao'),
    path('gastos/adicionar/', AdicionarGastoView.as_view(), name='adicionar_gasto'),
    path('gastos/editar/<int:pk>/', EditarGastoView.as_view(), name='editar_gasto'),
    path('relatorio/gastos/', RelatorioGastosView.as_view(), name='relatorio_gastos'),
    path('cadastro/', cadastro_categoria, name='cadastro_categoria'),  # Corrigido aqui
    path('adicionar/', AdicionarCartaoView.as_view(), name='adicionar_cartao'),
    path('cartao/<int:cartao_id>/editar/', editar_cartao, name='editar_cartao'),
    path('cartao/excluir/<int:pk>/', excluir_cartao_view, name='excluir_cartao'),
    path('gasto/excluir/<int:gasto_id>/', views.excluir_gasto, name='excluir_gasto'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

