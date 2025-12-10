# backend/cadastro/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # Esta rota irá lidar com POST (Criar) e GET (Listar)
    path('', views.leads_list, name='leads_list'), 
    
    path('bitrix-list/', views.listar_leads_bitrix, name='listar_leads_bitrix'),
]