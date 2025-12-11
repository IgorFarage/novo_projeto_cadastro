from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from .services.bitrix import BitrixService, BitrixConnectionError
from .services.mock_bitrix import MockBitrixService
from .models import Lead
from .serializers import LeadSerializer
import os
from rest_framework.permissions import IsAuthenticated 
from django.http import HttpResponse # Para o proxy de imagens
from decimal import Decimal # Importar para lidar com dinheiro com precisão
import random # Para a simulação de pagamento
import requests
# Importe os novos módulos/models/serializers
from .models import Order, OrderItem 
from .serializers import CheckoutSerializer

# Obtém a URL do Webhook do arquivo .env
BITRIX_WEBHOOK_URL = os.getenv('BITRIX_WEBHOOK_URL')

@api_view(['POST', 'GET'])
def leads_list(request):
    """
    Lista todos os leads (GET) ou cria um novo lead (POST)
    integrado com o Bitrix24.
    """
    
    # === LÓGICA DE LISTAGEM (GET) ===
    if request.method == 'GET':
        leads = Lead.objects.all().order_by('-id')
        serializer = LeadSerializer(leads, many=True)
        return Response(serializer.data)

    # === LÓGICA DE CRIAÇÃO (POST) ===
    elif request.method == 'POST':
        serializer = LeadSerializer(data=request.data)
        
        if serializer.is_valid():
            # 1. SALVAR LOCALMENTE (POSTGRES)
            # Primeiro salvamos no banco local para garantir que temos os dados
            lead_instance = serializer.save()
            
            # 2. ENVIAR PARA BITRIX (Integração)
            try:
                # Monta a URL do método do Bitrix
                url_final = f"{BITRIX_WEBHOOK_URL}/crm.lead.add"
                
                # Monta o JSON (Payload) exatamente como o Bitrix espera
                # Usamos os dados salvos em 'lead_instance'
                payload_bitrix = {
                    "fields": {
                        # Título do Lead no CRM
                        "TITLE": f"Lead do Site: {lead_instance.nome} {lead_instance.sobrenome or ''}",
                        
                        # Dados Pessoais
                        "NAME": lead_instance.nome,
                        "LAST_NAME": lead_instance.sobrenome,
                        "STATUS_ID": "NEW",
                        "OPENED": "Y",

                        # Telefone (Estrutura de lista do Bitrix)
                        "PHONE": [ 
                            { "VALUE": lead_instance.telefone, "VALUE_TYPE": "WORK" } 
                        ],
                        
                        # Email (Estrutura de lista do Bitrix)
                        "EMAIL": [
                            { "VALUE": lead_instance.email, "VALUE_TYPE": "WORK" }
                        ],

                        # Endereço Completo
                        "ADDRESS_STREET": lead_instance.endereco_rua,
                        "ADDRESS_CITY": lead_instance.endereco_cidade,
                        "ADDRESS_PROVINCE": lead_instance.endereco_estado,
                        "ADDRESS_POSTAL_CODE": lead_instance.endereco_cep,
                        "ADDRESS_COUNTRY": lead_instance.endereco_pais,
                    },
                    "params": {
                        "REGISTER_SONET_EVENT": "Y" # Registra histórico no CRM
                    }
                }
                
                # Faz o envio para o Bitrix
                resp_bitrix = requests.post(url_final, json=payload_bitrix)
                
                # Verifica se o Bitrix aceitou (Status 200 e campo 'result' na resposta)
                if resp_bitrix.status_code == 200 and 'result' in resp_bitrix.json():
                    id_bitrix = resp_bitrix.json()['result']
                    
                    # Atualiza o lead local com o ID gerado pelo Bitrix
                    lead_instance.bitrix_id = id_bitrix
                    lead_instance.save()
                    
                    return Response({
                        "mensagem": "Cadastro completo!", 
                        "id_interno": lead_instance.id,
                        "id_bitrix": id_bitrix
                    }, status=status.HTTP_201_CREATED)
                
                else:
                    # Caso salve no banco local, mas o Bitrix recuse ou dê erro
                    return Response({
                        "mensagem": "Salvo localmente. Falha no Bitrix.",
                        "detalhe": resp_bitrix.text
                    }, status=status.HTTP_206_PARTIAL_CONTENT)

            except Exception as e:
                # Caso haja erro de conexão (internet caiu, url errada, etc)
                return Response({
                    "mensagem": "Salvo localmente. Erro de conexão com CRM.",
                    "detalhe": str(e)
                }, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        
        # Caso os dados enviados pelo React estejam inválidos (ex: email sem @)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Adicione estes imports se não existirem
# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.permissions import IsAuthenticated

@api_view(['GET'])
# @permission_classes([IsAuthenticated]) # Garante que só logados vejam (Opcional se já estiver no settings global)
def listar_leads_bitrix(request):
    """
    Consulta os Leads diretamente do Bitrix24 e retorna para o Frontend.
    """
    try:
        # Método do Bitrix para listar leads
        url_bitrix = f"{BITRIX_WEBHOOK_URL}/crm.lead.list"
        
        # Parâmetros para filtrar e selecionar campos específicos
        # 'select': Quais campos queremos trazer (reduz tráfego)
        # 'order': Ordenação (DESC = Decrescente por ID)
        payload = {
            "select": ["ID", "TITLE", "NAME", "LAST_NAME", "STATUS_ID", "OPPORTUNITY", "DATE_CREATE"],
            "order": { "ID": "DESC" }
        }
        
        # Faz a chamada segura servidor-servidor
        response = requests.post(url_bitrix, json=payload)
        
        if response.status_code == 200:
            dados = response.json()
            # O Bitrix retorna os leads dentro de 'result'
            lista_leads = dados.get('result', [])
            return Response(lista_leads, status=status.HTTP_200_OK)
        else:
            return Response({
                "erro": "Bitrix recusou a conexão", 
                "detalhe": response.text
            }, status=status.HTTP_502_BAD_GATEWAY)

    except Exception as e:
        return Response({"erro": "Falha interna ao conectar com Bitrix", "detalhe": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

from rest_framework.permissions import IsAuthenticated, AllowAny

class ImageProxyView(APIView):
    """
    Proxy reverso para servir imagens do Bitrix e evitar bloqueio CORB/CORS no navegador.
    O frontend solicita a imagem para este endpoint, e o backend baixa do Bitrix.
    """
    permission_classes = [AllowAny]

    def get(self, request):
        image_url = request.query_params.get('url')
        if not image_url:
            return Response({'error': 'URL not provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Validação de segurança básica: Permitir apenas domínios Bitrix
        valid_domains = ['bitrix24.com', 'bitrix24.com.br', 'cdn.bitrix24.com.br']
        if not any(domain in image_url for domain in valid_domains):
            return Response({'error': 'Invalid domain'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Baixa a imagem do Bitrix (stream=True para não carregar grandes arquivos em memória)
            response = requests.get(image_url, stream=True, timeout=10)
            
            if response.status_code == 200:
                # Retorna a imagem com o content-type original
                return HttpResponse(
                    response.content, 
                    content_type=response.headers.get('Content-Type')
                )
            else:
                return Response({'error': 'Failed to fetch image'}, status=response.status_code)
                
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ProductListView(APIView):
    """
    Endpoint que atua como proxy para listar produtos do Bitrix24.
    Usa MockBitrixService como fallback se Bitrix24 falhar.
    """
    def get(self, request):
        try:
            # Tenta usar o Bitrix real primeiro
            service = BitrixService()
            products_raw = service.get_products()
            
        except BitrixConnectionError as e:
            # Se Bitrix falhar, usa o mock service
            print(f"⚠️  Bitrix falhou, usando MOCK service: {e}")
            service = MockBitrixService()
            products_raw = service.get_products()
            
        except Exception as e:
            # Erro inesperado, tenta mock como último recurso
            print(f"⚠️  Erro inesperado, usando MOCK service: {e}")
            service = MockBitrixService()
            products_raw = service.get_products()
        
        try:
            # Tratamento de dados: Padroniza o JSON retornado pelo Bitrix para o Frontend
            products_cleaned = []
            
            # Base URL para o Proxy
            # Em produção, use request.build_absolute_uri
            proxy_base_url = "http://127.0.0.1:8000/api/cadastro/proxy-image/?url="
            
            for p in products_raw:
                product_id = p.get("id", p.get("ID"))
                price = p.get("purchasingPrice", p.get("PRICE", 0))
                
                # Busca imagem real do Bitrix
                # Fallback para placeholder se não encontrar
                image_url = "https://via.placeholder.com/200x200/cccccc/000000?text=Sem+Imagem" 
                
                try:
                    images = service.get_product_images(product_id)
                    if images and len(images) > 0:
                        first_image = images[0]
                        original_url = first_image.get("downloadUrl") or first_image.get("src")
                        
                        if original_url:
                            # Constrói a URL do Proxy
                            import urllib.parse
                            encoded_url = urllib.parse.quote(original_url)
                            image_url = f"{proxy_base_url}{encoded_url}"
                            print(f"🖼️ Proxy configurado para produto {product_id}")
                            
                except Exception as e:
                    print(f"⚠️ Erro imagem produto {product_id}: {e}")
                
                products_cleaned.append({
                    "id": product_id,
                    "name": p.get("name", p.get("NAME")),
                    "price": float(price) if price else 0.0, 
                    "currency": p.get("purchasingCurrency", p.get("CURRENCY_ID", "BRL")),
                    "image": image_url, 
                    "description": p.get("previewText", p.get("DESCRIPTION", ""))
                })
                
            return Response(products_cleaned, status=status.HTTP_200_OK)
            
        except Exception as e:
             # Erro genérico (ex: problema de JSON inválido)
             print(f"Erro inesperado ao processar produtos: {e}")
             return Response(
                {"detail": "Ocorreu um erro interno ao processar a lista de produtos."}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )





class CheckoutView(APIView):
    """
    Processa a finalização da compra: valida carrinho, simula pagamento, salva no DB e envia para Bitrix.
    """
    permission_classes = [IsAuthenticated] 

    def post(self, request):
        serializer = CheckoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        cart_items_input = data['items']
        
        # 1. VALIDAÇÃO E CÁLCULO DE PREÇOS (BACKEND SÓ CONFIA NO BITRIX)
        bitrix_service = BitrixService()
        total_amount = Decimal('0.00')
        processed_items = []

        try:
            for item in cart_items_input:
                product_id = item['bitrix_product_id']
                quantity = item['quantity']

                # Busca o preço real do produto no Bitrix
                bitrix_product = bitrix_service.get_product_by_id(product_id)
                
                if not bitrix_product:
                    return Response(
                        {"detail": f"Produto com ID {product_id} não encontrado ou inativo."}, 
                        status=status.HTTP_400_BAD_REQUEST
                    )

                unit_price = Decimal(bitrix_product.get('PRICE', 0))
                item_total = unit_price * quantity
                total_amount += item_total
                
                processed_items.append({
                    'bitrix_product_id': product_id,
                    'product_name': bitrix_product.get('NAME', 'Produto Desconhecido'),
                    'unit_price': unit_price,
                    'quantity': quantity,
                })

        except BitrixConnectionError as e:
             return Response({"detail": str(e)}, status=BitrixConnectionError.status_code)
        except Exception as e:
             return Response({"detail": f"Erro inesperado no cálculo: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


        # 2. SIMULAÇÃO DE PAGAMENTO
        card_number = data['card_number']
        transaction_id = f"FAKE-{random.randint(100000, 999999)}"
        new_status = 'PENDING'
        
        # Regra: Final 1 = Aprovado, Final 2 = Recusado.
        last_digit = card_number[-1] 
        
        if last_digit == '1':
            new_status = 'PAID'
            payment_message = "Pagamento APROVADO com sucesso. Obrigado!"
        elif last_digit == '2':
            new_status = 'CANCELLED'
            payment_message = "Pagamento RECUSADO pela operadora. Tente outro cartão."
        else:
            new_status = 'PENDING'
            payment_message = "Pagamento em análise."
            
        # Se recusado, retorna erro e para por aqui
        if new_status == 'CANCELLED':
            return Response({
                "detail": payment_message,
                "status": "payment_refused",
                "transaction_id": transaction_id,
            }, status=status.HTTP_402_PAYMENT_REQUIRED)


        # 3. SALVAR O PEDIDO (Persistência no Django)
        try:
            order = Order.objects.create(
                user=request.user, 
                status=new_status,
                total_amount=total_amount,
                endereco_completo=data['endereco_completo'],
                payment_processor_id=transaction_id
            )

            order_items_to_create = [
                OrderItem(order=order, **item_data)
                for item_data in processed_items
            ]
            OrderItem.objects.bulk_create(order_items_to_create)
            
            # 4. ENVIAR PARA O BITRIX (Integração)
            bitrix_order_data = {
                'order_id': order.id,
                'total_amount': total_amount,
                'items': processed_items
            }
            
            # Tenta criar o negócio no Bitrix
            bitrix_deal_id = None
            try:
                bitrix_deal_id = bitrix_service.create_bitrix_deal(
                    user=request.user, 
                    order_data=bitrix_order_data
                )
            except Exception as e:
                # Loga o erro mas não falha a requisição principal, pois a venda já ocorreu
                print(f"Alerta: Pedido {order.id} salvo, mas falhou ao enviar para Bitrix: {e}")

            return Response({
                "order_id": order.id,
                "total_paid": str(total_amount),
                "status": order.get_status_display(),
                "message": payment_message,
                "bitrix_deal_id": bitrix_deal_id
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            print(f"Erro ao salvar pedido: {e}")
            return Response({
                "detail": "Falha crítica ao salvar o pedido.", 
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)