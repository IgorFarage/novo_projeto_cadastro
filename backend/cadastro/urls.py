# backend/cadastro/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # Esta rota irá lidar com POST (Criar) e GET (Listar)
    path('', views.leads_list, name='leads_list'), 
    
    # Você também precisará da rota de detalhe para PUT e DELETE (próximos passos)
    # path('<int:pk>/', views.lead_detail, name='lead_detail'), 
]