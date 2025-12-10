from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Lead
from .serializers import LeadSerializer
import requests
import os

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