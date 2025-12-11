# File: backend/cadastro/services/mock_bitrix.py

"""
Mock Bitrix Service para testes sem depender do Bitrix24 real.
Use este serviço quando não tiver acesso ao Bitrix ou para desenvolvimento local.
"""

class MockBitrixService:
    """Serviço mock que simula respostas do Bitrix24"""
    
    def get_products(self):
        """Retorna produtos fake para teste"""
        return [
            {
                "ID": "1",
                "NAME": "Produto Teste 1",
                "PRICE": "99.90",
                "CURRENCY_ID": "BRL",
                "PREVIEW_PICTURE": None,
                "DESCRIPTION": "Descrição do produto teste 1"
            },
            {
                "ID": "2",
                "NAME": "Produto Teste 2",
                "PRICE": "149.90",
                "CURRENCY_ID": "BRL",
                "PREVIEW_PICTURE": None,
                "DESCRIPTION": "Descrição do produto teste 2"
            },
            {
                "ID": "3",
                "NAME": "Produto Teste 3",
                "PRICE": "199.90",
                "CURRENCY_ID": "BRL",
                "PREVIEW_PICTURE": None,
                "DESCRIPTION": "Descrição do produto teste 3"
            },
            {
                "ID": "4",
                "NAME": "Produto Teste 4",
                "PRICE": "79.90",
                "CURRENCY_ID": "BRL",
                "PREVIEW_PICTURE": None,
                "DESCRIPTION": "Descrição do produto teste 4"
            },
        ]
    
    def get_product_by_id(self, product_id):
        """Busca um produto específico por ID"""
        products = self.get_products()
        for product in products:
            if product["ID"] == str(product_id):
                return product
        return None
    
    def get_product_images(self, product_id):
        """Retorna lista vazia de imagens (mock não tem imagens)"""
        return []
    
    def create_bitrix_deal(self, user, order_data):
        """Simula criação de negócio no Bitrix"""
        # Retorna um ID fake de negócio
        import random
        fake_deal_id = random.randint(1000, 9999)
        print(f"[MOCK] Negócio criado com sucesso: ID {fake_deal_id}")
        print(f"[MOCK] Pedido #{order_data['order_id']} - Total: R$ {order_data['total_amount']}")
        return fake_deal_id
