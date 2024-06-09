from rest_framework import serializers
from .models import CustomUser, Cliente

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'nome_corretora', 'cnpj', 'url', 'endereco', 'pais', 'tipo_ni', 'tipo_de_registro']

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ['id', 'cpf_cnpj', 'nome', 'tipo_ni', 'endereco', 'pais', 'ni', 'corretora']
        read_only_fields = ['corretora']  # corretora não pode ser editado
