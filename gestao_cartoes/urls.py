# urls.py dentro da aplicação cartoes
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .views import gastos_do_cartao
from . import views
from .views import (
    AdicionarCartaoView,
    ListaCartoesView,
    DetalhesCartaoView,
    RelatorioGastosView,
    AdicionarGastoView,
    EditarGastoView,
    cadastro_categoria,
    editar_cartao,
    excluir_cartao_view,
    excluir_gasto,
    editar_categoria,
    excluir_categoria,
   
    
)

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('lista_cartoes/', ListaCartoesView.as_view(), name='lista_cartoes'),
    path('<int:pk>/', DetalhesCartaoView.as_view(), name='detalhes_cartao'),
    path('gastos/adicionar/', AdicionarGastoView.as_view(), name='adicionar_gasto'),
    path('gastos/editar/<int:pk>/', EditarGastoView.as_view(), name='editar_gasto'),
    path('relatorio/gastos/', RelatorioGastosView.as_view(), name='relatorio_gastos'),
    path('categorias/', cadastro_categoria, name='cadastro_categoria'),
    path('categorias/editar/<int:categoria_id>/', editar_categoria, name='editar_categoria'),
    path('categorias/excluir/<int:categoria_id>/', excluir_categoria, name='excluir_categoria'),
    path('adicionar/', AdicionarCartaoView.as_view(), name='adicionar_cartao'),
    path('cartao/<int:cartao_id>/editar/', editar_cartao, name='editar_cartao'),
    path('cartao/excluir/<int:pk>/', excluir_cartao_view, name='excluir_cartao'),
    path('gasto/excluir/<int:gasto_id>/', excluir_gasto, name='excluir_gasto'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('cartao/<int:cartao_id>/gastos/', gastos_do_cartao, name='gastos_do_cartao'),
   
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
