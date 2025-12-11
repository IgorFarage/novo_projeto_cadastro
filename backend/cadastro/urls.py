# backend/cadastro/urls.py

from django.urls import path
from . import views
from .views import ProductListView, CheckoutView

urlpatterns = [
    path('proxy-image/', views.ImageProxyView.as_view(), name='proxy_image'),

    # Esta rota irá lidar com POST (Criar) e GET (Listar)
    path('', views.leads_list, name='leads_list'), 
    
    path('bitrix-list/', views.listar_leads_bitrix, name='listar_leads_bitrix'),

    path('products/', ProductListView.as_view(), name='product-list'),

    path('checkout/', CheckoutView.as_view(), name='checkout-process'),
]