from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Lead(models.Model):
    
    # --- Campos Básicos ---
    nome = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=20, blank=True, null=True)
    
    # --- NOVOS CAMPOS (Adicionados para correção) ---
    sobrenome = models.CharField(max_length=255, blank=True, null=True)
    endereco_rua = models.CharField(max_length=255, blank=True, null=True)
    endereco_cidade = models.CharField(max_length=100, blank=True, null=True)
    endereco_estado = models.CharField(max_length=50, blank=True, null=True)
    endereco_cep = models.CharField(max_length=20, blank=True, null=True)
    # Valor padrão 'Brasil' facilita se o usuário não preencher
    endereco_pais = models.CharField(max_length=50, default='Brasil')

    # --- Campos de Controle ---
    bitrix_id = models.IntegerField(null=True, blank=True)
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nome} {self.sobrenome or ''}"

class Order(models.Model):
    # Relacionamento com o usuário que fez a compra.
    # on_delete=models.SET_NULL: Se o usuário for deletado, o pedido permanece (com 'user' Nulo).
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Status do pedido
    STATUS_CHOICES = [
        ('PENDING', 'Pendente de Pagamento'),
        ('PROCESSING', 'Em Processamento'),
        ('PAID', 'Pago/Aprovado'),
        ('SHIPPED', 'Enviado'),
        ('COMPLETED', 'Concluído'),
        ('CANCELLED', 'Cancelado'),
        ('REFUNDED', 'Reembolsado'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')

    # Endereço de Entrega (simples, reuso dos campos de Lead se for o caso)
    # Para ser produção, seria bom um modelo Address separado ou buscar os campos aqui.
    endereco_completo = models.TextField(blank=True, verbose_name="Endereço de Entrega")
    
    # Valores
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    # Datas de Rastreio
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Campos de Simulação de Pagamento
    payment_processor_id = models.CharField(max_length=255, blank=True, null=True, verbose_name="ID da Transação Fake")
    
    def __str__(self):
        return f"Pedido {self.id} - {self.get_status_display()}"

    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"
        ordering = ['-created_at']


class OrderItem(models.Model):
    # Relacionamento com o pedido. CASCADE: Se o pedido for deletado, os itens dele vão junto.
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    
    # ID Externo do Produto (Bitrix ID)
    bitrix_product_id = models.CharField(max_length=50, verbose_name="ID do Produto no Bitrix")
    
    # Informações congeladas do produto no momento da compra
    product_name = models.CharField(max_length=255)
    
    # Preço unitário no momento da compra (IMPORTANTE: Garante o histórico, mesmo se o preço mudar no Bitrix)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    quantity = models.PositiveIntegerField(default=1)
    
    # Calcula o subtotal do item
    @property
    def subtotal(self):
        return self.unit_price * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.product_name} (Pedido {self.order.id})"

    class Meta:
        verbose_name = "Item do Pedido"
        verbose_name_plural = "Itens do Pedido"
        unique_together = ('order', 'bitrix_product_id') # Garante que não haja duplicidade do mesmo produto no mesmo pedido