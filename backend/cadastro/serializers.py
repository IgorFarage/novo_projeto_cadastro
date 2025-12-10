from rest_framework import serializers
from .models import Lead

class LeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        fields = [
            'id', 'nome', 'email', 'telefone', 
            # NOVOS CAMPOS:
            'sobrenome', 'endereco_rua', 'endereco_cidade', 'endereco_estado', 'endereco_cep', 'endereco_pais',
            # FIM NOVOS CAMPOS
            'bitrix_id', 'data_criacao'
        ]
        read_only_fields = ['id', 'bitrix_id', 'data_criacao']