from django import forms
from .models import Formulario, FormularioFinal
from utils.cripto_data import tipos_ni, tipos_registro, codigos_operacao

class FormularioForm(forms.ModelForm):
    class Meta:
        model = Formulario
        fields = [
            'cliente', 'tipo_registro', 'data_operacao', 'codigo_operacao', 
            'valor_operacao', 'valor_taxas', 'simbolo_criptoativo', 'quantidade_criptoativo', 
            'numero_nota_fiscal', 'hash_criptoativo'
        ]
        widgets = {
            'data_operacao': forms.DateInput(attrs={'type': 'date'}),
        }
        help_texts = {
            'cliente': 'Selecione o cliente para esta operação.',
            'tipo_registro': 'Código do tipo de registro conforme tabela do manual.',
            'data_operacao': 'Data da operação no formato DDMMAAAA.',
            'codigo_operacao': 'Código da operação conforme tabela de código.',
            'valor_operacao': 'Valor da operação em reais excluídas as taxas.',
            'valor_taxas': 'Valor das taxas em reais cobradas na operação.',
            'simbolo_criptoativo': 'Símbolo do criptoativo. Ex: BTC para bitcoin, ETH para Ethereum, etc.',
            'quantidade_criptoativo': 'Quantidade de criptoativos comprados.',
            'numero_nota_fiscal': 'Número da nota fiscal da operação.',
            'hash_criptoativo': 'Hash do criptoativo.',
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['codigo_operacao'].required = False

    def clean_codigo_operacao(self):
        codigo_operacao = self.cleaned_data.get('codigo_operacao')
        tipo_registro = self.cleaned_data.get('tipo_registro')

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
        return codigo_operacao

    def clean(self):
        cleaned_data = super().clean()
        cliente = cleaned_data.get('cliente')
        tipo_registro = cleaned_data.get('tipo_registro')

        # Verificar se o cliente pertence à corretora logada
        if cliente and cliente.corretora != self.user:
            raise forms.ValidationError("Você não tem permissão para adicionar este cliente.")

        # Automatizar campos específicos para tipos de registro
        if tipo_registro in ['0110', '0210', '0410', '0510', '0710']:
            if not cleaned_data.get('numero_nota_fiscal'):
                cleaned_data['numero_nota_fiscal'] = self.instance.gerar_numero_nota_fiscal()
            if not cleaned_data.get('valor_taxas'):
                cleaned_data['valor_taxas'] = 0.00
            if not cleaned_data.get('hash_criptoativo'):
                cleaned_data['hash_criptoativo'] = self.instance.gerar_hash_criptoativo()

        return cleaned_data

class FormularioFinalForm(forms.ModelForm):
    class Meta:
        model = FormularioFinal
        fields = ['data_inicial', 'data_final']
        widgets = {
            'data_inicial': forms.DateInput(attrs={'type': 'date'}),
            'data_final': forms.DateInput(attrs={'type': 'date'}),
        }
        help_texts = {
            'data_inicial': 'Data inicial do período para o formulário final.',
            'data_final': 'Data final do período para o formulário final.',
        }
