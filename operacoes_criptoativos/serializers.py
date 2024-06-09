from rest_framework import serializers
from .models import Formulario,FormularioFinal

class FormularioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Formulario
        fields = [
            'usuario', 'cliente', 'tipo_registro', 'data_operacao', 'codigo_operacao', 
            'valor_operacao', 'valor_taxas', 'simbolo_criptoativo', 'quantidade_criptoativo', 
            'numero_nota_fiscal', 'hash_criptoativo', 'registro'
        ]
        read_only_fields = ['usuario', 'registro']

    def validate_codigo_operacao(self, value):
        tipo_registro = self.initial_data.get('tipo_registro')

        # Definir códigos de operação com base no tipo de registro
        if tipo_registro == '0110':
            return 'I'
        elif tipo_registro == '0210':
            return 'II'
        elif tipo_registro == '0410':
            return 'IV'
        elif tipo_registro == '0510':
            return 'V'
        elif tipo_registro == '0710':
            return 'VII'
        return value

    def validate(self, data):
        tipo_registro = data.get('tipo_registro')
        cliente = data.get('cliente')
        usuario = self.context['request'].user

        # Verificar se o cliente pertence à corretora logada
        if cliente and cliente.corretora != usuario:
            raise serializers.ValidationError("Você não tem permissão para adicionar este cliente.")

        # Automatizar campos específicos para tipos de registro
        instance = self.instance or Formulario()
        if tipo_registro in ['0110', '0210', '0410', '0510', '0710']:
            if not data.get('numero_nota_fiscal'):
                data['numero_nota_fiscal'] = instance.gerar_numero_nota_fiscal()
            if not data.get('valor_taxas'):
                data['valor_taxas'] = 0
            if not data.get('hash_criptoativo'):
                data['hash_criptoativo'] = instance.gerar_hash_criptoativo()

        return data


class FormularioFinalSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormularioFinal
        fields = '__all__'
        read_only_fields = ('usuario',)

    def create(self, validated_data):
        validated_data['usuario'] = self.context['request'].user
        return super().create(validated_data)