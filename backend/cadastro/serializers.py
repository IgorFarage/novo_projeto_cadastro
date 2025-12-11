from rest_framework import serializers
from .models import Lead, Order, OrderItem

class LeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        # Precisamos listar EXPLICITAMENTE os novos campos aqui
        fields = [
            'id', 
            'nome', 
            'sobrenome',       # Novo
            'email', 
            'telefone', 
            'endereco_rua',    # Novo
            'endereco_cidade', # Novo
            'endereco_estado', # Novo
            'endereco_cep',    # Novo
            'endereco_pais',   # Novo
            'bitrix_id', 
            'data_criacao'
        ]
        read_only_fields = ['id', 'bitrix_id', 'data_criacao']

class OrderItemInputSerializer(serializers.Serializer):
    """
    Serializer para validar a lista de itens enviados pelo Frontend.
    """
    # bitrix_product_id: ID do produto que vem do Bitrix (deve ser uma string)
    bitrix_product_id = serializers.CharField(max_length=50) 
    # quantity: A quantidade deve ser um inteiro positivo.
    quantity = serializers.IntegerField(min_value=1)

class CheckoutSerializer(serializers.Serializer):
    """
    Serializer principal para validar todos os dados necessários no checkout.
    """
    # Endereço: Simples, para fins de simulação.
    endereco_completo = serializers.CharField(max_length=500) 
    
    # Itens: Usa o OrderItemInputSerializer para validar a lista
    items = OrderItemInputSerializer(many=True) 

    # --- Dados Fictícios do Cartão de Crédito ---
    # Em produção, esses dados iriam para um gateway (Stripe, PagSeguro, etc.)
    card_number = serializers.CharField(max_length=16, min_length=16)
    card_holder_name = serializers.CharField(max_length=255)
    expiry_date = serializers.CharField(max_length=5) # MM/YY
    cvv = serializers.CharField(max_length=4)
    
    # Campo para checagem de segurança e regras de negócio
    def validate_items(self, value):
        if not value:
            raise serializers.ValidationError("O carrinho não pode estar vazio.")
        
        # Opcional: checar por IDs duplicados no carrinho antes de processar
        ids = [item['bitrix_product_id'] for item in value]
        if len(ids) != len(set(ids)):
            raise serializers.ValidationError("Itens duplicados encontrados no carrinho.")
            
        return value