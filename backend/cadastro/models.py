from django.db import models

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