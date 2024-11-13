from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .views import editar_cartao  # Certifique-se de importar a função de view corretamente.
from .views import excluir_cartao  # Certifique-se de que a view está sendo importada corretamente

from .views import (
    ListaCartoesView,
    DetalhesCartaoView,
    AdicionarCartaoView,
    AdicionarGastoView,
    EditarGastoView,
    RelatorioGastosView,
    cadastro_categoria,
    excluir_gasto,
    gastos_do_cartao,
    register,
    
)

urlpatterns = [
    # Autenticação
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),  # Adiciona logout aqui
    path('register/', register, name='register'),

    # Cartões
    path('lista_cartoes/', ListaCartoesView.as_view(), name='lista_cartoes'),
    path('cartao/<int:pk>/', DetalhesCartaoView.as_view(), name='detalhes_cartao'),
    path('cartao/adicionar/', AdicionarCartaoView.as_view(), name='adicionar_cartao'),
    path('cartao/<int:pk>/editar/', editar_cartao, name='editar_cartao'),
     path('cartao/<int:pk>/excluir/', excluir_cartao, name='excluir_cartao'),
     path('cartao/<int:cartao_id>/gastos/', gastos_do_cartao, name='gastos_do_cartao'),


    # Gastos
    path('gastos/adicionar/', AdicionarGastoView.as_view(), name='adicionar_gasto'),
    path('gastos/editar/<int:pk>/', EditarGastoView.as_view(), name='editar_gasto'),
    path('cartao/<int:cartao_id>/gastos/', gastos_do_cartao, name='gastos_do_cartao'),
    path('gasto/excluir/<int:gasto_id>/', excluir_gasto, name='excluir_gasto'),
    
     path('categorias/', cadastro_categoria, name='cadastro_categoria'),

    # Relatórios
    path('relatorio/gastos/', RelatorioGastosView.as_view(), name='relatorio_gastos'),
]

# Configuração de arquivos estáticos em ambiente de desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
