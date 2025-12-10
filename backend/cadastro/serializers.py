from rest_framework import serializers
from .models import Lead

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