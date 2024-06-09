from django import forms
from accounts.models import Cliente
from .models import Formulario

class FormularioForm(forms.ModelForm):
    class Meta:
        model = Formulario
        fields = [
            'cliente', 'tipo_registro', 'data_operacao', 'codigo_operacao', 'valor_operacao',
            'valor_taxas', 'simbolo_criptoativo', 'quantidade_criptoativo', 'numero_nota_fiscal', 'hash_criptoativo'
        ]
        help_texts = {
            'cliente': 'Selecione o cliente (comprador) para esta operação.',
            'data_operacao': 'Insira a data em que a operação foi realizada.',
            'codigo_operacao': 'Código da operação conforme tabela de código (I para compra e venda).',
            'valor_operacao': 'Valor da operação em reais excluídas as taxas.',
            'valor_taxas': 'Valor das taxas em reais cobradas na operação.',
            'simbolo_criptoativo': 'Símbolo do criptoativo (ex: BTC para Bitcoin, ETH para Ethereum).',
            'quantidade_criptoativo': 'Quantidade de criptoativos comprados.',
            'numero_nota_fiscal': 'Número da nota fiscal da operação.',
            'hash_criptoativo': 'Hash do criptoativo.',
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(FormularioForm, self).__init__(*args, **kwargs)
        if self.user:
            self.fields['cliente'].queryset = Cliente.objects.filter(corretora=self.user)
