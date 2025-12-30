# backend/pagamentos/views.py

import mercadopago
import os
import json # Importado para melhorar o print
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from dotenv import load_dotenv

load_dotenv()

# Configuração do SDK
token = os.getenv("MP_ACCESS_TOKEN")
#if not token:
#    token = "TEST-TOKEN-FALSO"
sdk = mercadopago.SDK(token)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def processar_pagamento(request):
    try:
        # 1. Imprime o que chegou do Frontend (React)
        print("\n📦 1. DADOS RECEBIDOS DO REACT:")
        print(json.dumps(request.data, indent=2))

        request_values = request.data
        payment_method_id = request_values.get("payment_method_id")

        # ---------------------------------------------------------
        # LÓGICA DE MONTAGEM DO PACOTE (AQUI ESTÁ A CORREÇÃO)
        # ---------------------------------------------------------
        
        # 1. Dados COMUNS (que todo mundo tem: Valor, Descrição, Email)
        payer_data = {
            "email": request_values.get("payer", {}).get("email")
        }

        # Tenta pegar o CPF se ele veio (O Pix PRECISARÁ disso)
        doc_type = request_values.get("payer", {}).get("identification", {}).get("type")
        doc_number = request_values.get("payer", {}).get("identification", {}).get("number")

        if doc_type and doc_number:
            payer_data["identification"] = {
                "type": doc_type,
                "number": doc_number
            }

        payment_data = {
            "transaction_amount": float(request_values.get("transaction_amount")),
            "description": "Produto ProtocoloMed Teste",
            "payment_method_id": payment_method_id,
            "payer": payer_data
        }

        # 2. Dados ESPECÍFICOS DE CARTÃO (Só adiciona se NÃO for Pix)
        if payment_method_id != "pix":
            payment_data["token"] = request_values.get("token")
            payment_data["issuer_id"] = request_values.get("issuer_id")
            # Só converte pra int se for cartão, pois Pix não tem installments e dava erro aqui
            payment_data["installments"] = int(request_values.get("installments"))

        print("\n🚀 2. DADOS SENDO ENVIADOS PRO MERCADO PAGO:")
        print(json.dumps(payment_data, indent=2))

        # 3. Chamada ao SDK
        payment_response = sdk.payment().create(payment_data)

        # 4. Imprime a resposta
        print("\n📡 3. RESPOSTA CRUA DO MERCADO PAGO:")
        print(json.dumps(payment_response, indent=2))
        print("-" * 30)

        # Lógica de Resposta
        mp_status = payment_response.get("status")
        mp_response = payment_response.get("response", {})

        # Pix retorna status "pending" (criado), Cartão retorna "approved"
        # Então aceitamos 201 created para ambos
        if mp_status == 201:
            return Response({
                "mensagem": "Processamento iniciado!",
                "id_pagamento": mp_response.get("id"),
                "status": mp_response.get("status"),
                "qr_code": mp_response.get("point_of_interaction", {})
                                    .get("transaction_data", {})
                                    .get("qr_code"), # Para o Pix Copia e Cola
                "qr_code_base64": mp_response.get("point_of_interaction", {})
                                            .get("transaction_data", {})
                                            .get("qr_code_base64") # Para a imagem do QR
            }, status=status.HTTP_201_CREATED)
        
        else:
            return Response({
                "mensagem": "Erro no Mercado Pago",
                "erro_mp": mp_response
            }, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        print(f"\n☠️ ERRO INTERNO DO PYTHON: {str(e)}")
        return Response(
            {"erro": "Erro interno no servidor", "detalhe": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )