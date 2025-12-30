from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Painel Administrativo do Django
    path('admin/', admin.site.urls),
    
    # Rotas da nossa Aplicação de Cadastro (Leads)
    path('api/cadastro/', include('cadastro.urls')),

    # --- ROTAS DE AUTENTICAÇÃO (NOVO) ---
    
    # 1. Rotas do Djoser (Gerenciamento de Usuários)
    # Cria automaticamente:
    # POST /auth/users/ -> Registrar novo usuário
    # GET  /auth/users/me/ -> Dados do usuário logado (com Token)
    path('auth/', include('djoser.urls')),

    # 2. Rotas do JWT (Login e Tokens)
    # Cria automaticamente:
    # POST /auth/jwt/create/ -> Fazer Login (recebe user/pass, retorna tokens)
    # POST /auth/jwt/refresh/ -> Renovar o token vencido
    path('auth/', include('djoser.urls.jwt')),

    # --- Rotas de Pagamento ---
    path('api/pagamentos/', include('pagamentos.urls')),
]