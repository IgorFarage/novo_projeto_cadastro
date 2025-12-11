# File: backend/cadastro/admin.py

from django.contrib import admin
# Importar os novos modelos
from .models import Lead, Order, OrderItem 

# ... (LeadAdmin existente) ...

# Inline para mostrar os itens dentro da tela de Pedido
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    # Define campos de visualização
    fields = ['bitrix_product_id', 'product_name', 'unit_price', 'quantity', 'subtotal']
    readonly_fields = ['subtotal']
    extra = 0 # Não mostra linhas vazias por padrão


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'total_amount', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['user__email', 'id']
    readonly_fields = ['created_at', 'updated_at', 'total_amount', 'payment_processor_id']
    inlines = [OrderItemInline]
    
    # Garante que o total seja recalculado no salvamento (se necessário)
    def save_model(self, request, obj, form, change):
        # Recalcula o total apenas para garantir que a soma dos itens esteja correta
        # (O cálculo principal deve ser feito no checkout, mas isso é uma segurança)
        obj.total_amount = sum(item.subtotal for item in obj.items.all())
        super().save_model(request, obj, form, change)