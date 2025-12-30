# backend/pagamentos/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # A rota final será: /api/pagamentos/processar/
    path('processar/', views.processar_pagamento, name='processar_pagamento'),
]