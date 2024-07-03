# cartoes/urls.py
# cartoes/urls.py
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect
from django.contrib.auth import views as auth_views
from gestao_cartoes import views as gestao_views  # Importando as views do app gestao_cartoes

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lambda request: redirect('login/', permanent=False)),  # Redireciona para a página de login
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('register/', gestao_views.register, name='register'),  # URL para o cadastro de usuário
    path('gestao_cartoes/', include('gestao_cartoes.urls')),  # URLs do app gestao_cartoes
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
