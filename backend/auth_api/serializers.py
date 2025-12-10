# backend/auth_api/serializers.py

from djoser.serializers import UserSerializer as DjoserUserSerializer
from django.contrib.auth.models import User

# Serializer customizado para o Djoser
class UserSerializer(DjoserUserSerializer):
    class Meta(DjoserUserSerializer.Meta):
        model = User
        # Os campos que serão retornados ao acessar /auth/users/me/
        fields = ('id', 'username', 'email') 
        # Garante que o frontend não possa alterar id, email ou username
        read_only_fields = ('id', 'email', 'username')