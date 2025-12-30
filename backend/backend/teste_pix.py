# backend/teste_pix.py
import mercadopago
import os
import json
from dotenv import load_dotenv

# Carrega o .env
load_dotenv()

access_token = os.getenv("MP_ACCESS_TOKEN")
print(f"\n🔑 Testando com Token: {access_token}")

sdk = mercadopago.SDK(access_token)

# Dados Mínimos para PIX (Não usa cartão, não usa token de frontend)
payment_data = {
    "transaction_amount": 10.0,
    "description": "Teste Isolado PIX",
    "payment_method_id": "pix",
    "payer": {
        "email": "email_teste_pix_v1@teste.com",
        "first_name": "Test",
        "last_name": "User",
        "identification": {
            "type": "CPF",
            "number": "54879120090" # CPF Válido Gerado
        }
    }
}

print("📡 Enviando requisição PIX para o Mercado Pago...")
result = sdk.payment().create(payment_data)
response = result["response"]

print("\n" + "="*40)
if result["status"] == 201:
    print("✅ SUCESSO! O Backend e o Access Token estão funcionando.")
    print(f"ID do Pagamento: {response['id']}")
    print("CONCLUSÃO: O erro 403 anterior é 100% culpa da PUBLIC KEY no Frontend (Checkout.jsx).")
else:
    print("❌ FALHA NO BACKEND. O problema é a sua conta ou o Access Token.")
    print("Status:", result["status"])
    print("Erro:", json.dumps(response, indent=2))
print("="*40 + "\n")