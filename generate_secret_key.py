"""
Script para gerar uma SECRET_KEY segura para Django
Execute com: python generate_secret_key.py
"""
from django.core.management.utils import get_random_secret_key

if __name__ == "__main__":
    secret_key = get_random_secret_key()
    print("\n" + "="*60)
    print("🔑 NOVA SECRET_KEY GERADA:")
    print("="*60)
    print(f"\n{secret_key}\n")
    print("="*60)
    print("📋 Copie e cole no seu arquivo .env")
    print("="*60 + "\n")
