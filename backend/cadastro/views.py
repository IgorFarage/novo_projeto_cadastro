# backend/cadastro/views.py

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Lead
from .serializers import LeadSerializer
import requests
import os

# Variáveis de ambiente
BITRIX_WEBHOOK_URL = os.getenv('BITRIX_WEBHOOK_URL')

@api_view(['POST', 'GET'])
def leads_list(request):
    
    # Lógica 1: GET (Listagem)
    if request.method == 'GET':
        leads = Lead.objects.all().order_by('-id')
        serializer = LeadSerializer(leads, many=True)
        return Response(serializer.data)

    # Lógica 2: POST (Criação - Híbrida)
    elif request.method == 'POST':
        serializer = LeadSerializer(data=request.data)
        
        if serializer.is_valid():
            
            # 1. SALVAR LOCALMENTE (POSTGRES)
            lead_instance = serializer.save()
            
            # 2. ENVIAR PARA BITRIX
            try:
                url_final = f"{BITRIX_WEBHOOK_URL}/crm.lead.add"
                
                payload_bitrix = {
                    "fields": {
                        "TITLE": f"Lead do Site: {lead_instance.nome} {lead_instance.sobrenome or ''}",
                        "NAME": lead_instance.nome,
                        "LAST_NAME": lead_instance.sobrenome,
                        "STATUS_ID": "NEW",  
                        "OPENED": "Y",

                        "PHONE": [ 
                            { 
                                "VALUE": lead_instance.telefone, 
                                "VALUE_TYPE": "WORK" 
                            } 
                        ],
                        "EMAIL": [
                            {
                                "VALUE": lead_instance.email,
                                "VALUE_TYPE": "WORK"
                            }
                        ],

                        "ADDRESS": lead_instance.endereco_rua,
                        "ADDRESS_CITY": lead_instance.endereco_cidade,
                        "ADDRESS_PROVINCE": lead_instance.endereco_estado,
                        "ADDRESS_POSTAL_CODE": lead_instance.endereco_cep,
                        "ADDRESS_COUNTRY": lead_instance.endereco_pais,
                    },
                    "params": {
                        "REGISTER_SONET_EVENT": "Y"
                    }
                }
                
                resp_bitrix = requests.post(url_final, json=payload_bitrix)
                
                if resp_bitrix.status_code == 200 and 'result' in resp_bitrix.json():
                    id_bitrix = resp_bitrix.json()['result']
                    lead_instance.bitrix_id = id_bitrix
                    lead_instance.save()
                    
                    return Response({
                        "mensagem": "Cadastro completo!", 
                        "id_interno": lead_instance.id,
                        "id_bitrix": id_bitrix
                    }, status=status.HTTP_201_CREATED)
                
                else:
                    return Response({
                        "mensagem": "Salvo localmente. Falha no Bitrix.",
                        "detalhe": resp_bitrix.text
                    }, status=status.HTTP_206_PARTIAL_CONTENT)

            except Exception as e:
                return Response({"mensagem": "Salvo localmente. Erro de conexão com CRM.", "detalhe": str(e)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)