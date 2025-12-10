from django.shortcuts import render

from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60), # Token expira em 60 min
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),    # Login dura 1 dia
    'AUTH_HEADER_TYPES': ('Bearer',),               # Padrão OAuth
}

DJOSER = {
    'SERIALIZERS': {}, # Usa os serializers padrão seguros do Djoser
}

