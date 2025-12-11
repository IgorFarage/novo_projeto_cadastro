# File: backend/cadastro/services/bitrix.py

import requests
from django.conf import settings
from rest_framework.exceptions import APIException

# Exceção customizada para o serviço, essencial para um bom tratamento de erros na API
class BitrixConnectionError(APIException):
    status_code = 503
    default_detail = 'Não foi possível conectar-se ao serviço de produtos (Bitrix24).'
    default_code = 'bitrix_service_unavailable'

class BitrixService:
    def __init__(self):
        # Remove trailing slash if present to avoid double slashes
        self.base_url = settings.BITRIX_WEBHOOK_URL.rstrip('/') 

    def _call_bitrix_api(self, method, params=None):
        """Método privado para lidar com a comunicação HTTP e erros."""
        url = f"{self.base_url}/{method}"
        try:
            # Bitrix REST API usa POST com JSON no corpo, não GET com query params
            response = requests.post(url, json=params, timeout=10) 
            response.raise_for_status() # Lança exceção para códigos de status 4xx/5xx

            data = response.json()
            
            if "error" in data:
                # Trata erros retornados pelo Bitrix
                print(f"Erro da API Bitrix em {method}: {data.get('error_description', data.get('error'))}")
                raise BitrixConnectionError(f"Erro Bitrix: {data.get('error')}")

            return data.get("result", [])
                
        except requests.exceptions.RequestException as e:
            # Trata erros de conexão ou timeout
            print(f"Erro de conexão com Bitrix ({method}): {e}")
            raise BitrixConnectionError()

    def get_products(self):
        """Busca produtos usando crm.product.list (API estável e funcional)."""
        method = "crm.product.list"
        params = {
            "select": ["ID", "NAME", "PRICE", "CURRENCY_ID"],
            "filter": {"ACTIVE": "Y"}
        }
        return self._call_bitrix_api(method, params)

    def get_product_by_id(self, product_id):
        """Busca um único produto usando crm.product.get."""
        method = "crm.product.get"
        params = {"id": product_id}
        result = self._call_bitrix_api(method, params)
        return result if isinstance(result, dict) else None
    
    def get_product_images(self, product_id):
        """Busca imagens de um produto usando catalog.productImage.list."""
        method = "catalog.productImage.list"
        params = {
            "productId": product_id
        }
        try:
            result = self._call_bitrix_api(method, params)
            # Bitrix retorna {'productImages': [...]}
            if result and 'productImages' in result:
                return result['productImages']
            return []
        except BitrixConnectionError as e:
            print(f"❌ Erro ao buscar imagens: {e}")
            return []

    def create_bitrix_deal(self, user, order_data):
        """
        Cria um novo Negócio (Deal) e associa os Itens do Produto (Product Rows) no Bitrix.
        
        Args:
            user (User): O objeto User do Django.
            order_data (dict): Dados do pedido, incluindo total e itens processados.
        """
        method = "crm.deal.add"
        
        # 1. Preparar os dados do Negócio (Deal)
        deal_fields = {
            'TITLE': f"Pedido #{order_data['order_id']} - {user.email}",
            # Você precisa definir o ID do pipeline/status
            # Exemplo: 'C1:NEW' é o status 'Novo' no pipeline padrão (C1)
            'STAGE_ID': 'C1:NEW', 
            'OPPORTUNITY': str(order_data['total_amount']), # Valor total
            'CURRENCY_ID': 'BRL',
            # Associa ao usuário (Cria um contato ou busca o existente, 
            # assumindo que o campo NAME do Bitrix é o nome do Lead/User)
            'CONTACT_ID': None, # Será populado por uma busca se necessário
            # Campos customizados podem ser adicionados aqui (ex: ID do Pedido Django)
            # 'UF_CRM_12345': order_data['order_id'] 
        }

        # 2. Preparar os Itens do Produto para o Bitrix (Product Rows)
        product_rows = []
        for item in order_data['items']:
            product_rows.append({
                'PRODUCT_ID': item['bitrix_product_id'], # O ID do produto no Bitrix
                'PRICE': str(item['unit_price']),
                'QUANTITY': item['quantity'],
            })
            
        payload = {
            'fields': deal_fields,
            'params': {'REGISTER_SONET_EVENT': 'Y'},
            'productRows': product_rows,
        }

        # Em vez de 'get', crm.deal.add exige um 'POST'
        url = f"{self.base_url}/{method}"

        try:
            # Log do payload para debug
            print(f"🔵 Criando Deal no Bitrix...")
            print(f"Payload (sem products): {deal_fields}")
            
            # 1. Cria o Deal
            response = requests.post(url, json={'fields': deal_fields, 'params': {'REGISTER_SONET_EVENT': 'Y'}}, timeout=10)
            response.raise_for_status()
            result = response.json()
            
            if "result" in result:
                deal_id = result["result"]
                print(f"✅ Deal criado com sucesso! ID: {deal_id}")
                
                # 2. Adiciona os produtos ao Deal usando crm.deal.productrows.set
                # Essa abordagem é mais robusta que enviar junto com o deal.add
                if product_rows:
                    print(f"🔵 Adicionando produtos ao Deal {deal_id}...")
                    rows_method = "crm.deal.productrows.set"
                    rows_url = f"{self.base_url}/{rows_method}"
                    
                    rows_payload = {
                        'id': deal_id,
                        'rows': product_rows
                    }
                    
                    print(f"Payload Produtos: {rows_payload}")
                    rows_response = requests.post(rows_url, json=rows_payload, timeout=10)
                    rows_result = rows_response.json()
                    
                    if "result" in rows_result and rows_result["result"]:
                         print(f"✅ Produtos adicionados ao Deal {deal_id} com sucesso!")
                    else:
                         print(f"⚠️ Erro ao adicionar produtos: {rows_result}")

                return deal_id
            else:
                print(f"❌ Erro ao criar Deal: {result}")
                error_detail = result.get('error_description', result.get('error', 'Erro desconhecido ao criar Negócio.'))
                raise BitrixConnectionError(f"Falha na criação do Negócio Bitrix: {error_detail}")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Erro de conexão com Bitrix: {e}")
            if e.response:
                print(f"Detalhes: {e.response.text}")
            raise BitrixConnectionError(f"Erro de conexão ao criar Negócio no Bitrix: {e}")