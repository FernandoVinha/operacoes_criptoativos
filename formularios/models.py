import os
import uuid
import re
from django.db import models
from accounts.models import CustomUser

class Cliente(models.Model):
    corretora = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='clientes_criados')
    cpf_cnpj = models.CharField(max_length=20, help_text="CPF ou CNPJ do cliente.")  # CompradorCPFCNPJ:
    nome = models.CharField(max_length=80, help_text="Nome completo do cliente.")  # CompradorNome:
    tipo_ni = models.CharField(max_length=1, editable=False, help_text="Tipo de documento de identificação do cliente (1 para CPF, 2 para CNPJ).")  # CompradorTipoNI:
    endereco = models.CharField(max_length=120, help_text="Endereço completo do cliente.")  # CompradorEndereco:
    pais = models.CharField(max_length=2, help_text="Sigla do país do cliente.")  # CompradorPais:
    ni = models.CharField(max_length=30, blank=True, null=True, help_text="Número de identificação adicional do cliente (opcional).")

    def save(self, *args, **kwargs):
        self.cpf_cnpj = re.sub(r'\D', '', self.cpf_cnpj)
        if len(self.cpf_cnpj) == 11:
            self.tipo_ni = '1'  # CPF
        elif len(self.cpf_cnpj) == 14:
            self.tipo_ni = '2'  # CNPJ
        else:
            raise ValueError("CPF deve ter 11 dígitos e CNPJ deve ter 14 dígitos.")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nome


class OperacaoCompraVenda(models.Model):
    usuario = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    tipo_registro = models.CharField(max_length=4, default='0110', editable=False, help_text="Texto fixo contendo a identificação do registro (0110).")
    data_operacao = models.DateField(help_text="Data da operação no formato DDMMAAAA.")  # OperacaoData
    codigo_operacao = models.CharField(max_length=4, default='I', help_text="Código da operação conforme tabela de código (I para compra e venda).")
    valor_operacao = models.DecimalField(max_digits=15, decimal_places=2, help_text="Valor da operação em reais excluídas as taxas.")  # OperacaoValor:
    valor_taxas = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, help_text="Valor das taxas em reais cobradas na operação.")  # OperacaoTaxasValor
    simbolo_criptoativo = models.CharField(max_length=10, help_text="Símbolo do criptoativo. Ex: BTC para bitcoin, ETH para Ethereum, etc.")  # CriptoativoSimbolo
    quantidade_criptoativo = models.DecimalField(max_digits=26, decimal_places=10, help_text="Quantidade de criptoativos comprados.")  # CriptoativoQuantidade:
    numero_nota_fiscal = models.CharField(max_length=30, help_text="Número da nota fiscal da operação.")  # OperacaoID:
    hash_criptoativo = models.TextField(blank=True, null=True, help_text="Hash do criptoativo.")
    registro0110 = models.TextField(blank=True, null=True, editable=False, help_text="Campo preenchido automaticamente pelo sistema.")
    arquivo_registro = models.FileField(upload_to='registros/', blank=True, null=True, help_text="Arquivo de registro gerado automaticamente.")

    def __str__(self):
        return f"{self.codigo_operacao} - {self.simbolo_criptoativo} - {self.data_operacao}"

    def save(self, *args, **kwargs):
        if not self.id:  # Se for uma nova instância
            self.registro0110 = self.generate_registro0110()
        super().save(*args, **kwargs)
        self.generate_and_save_file()

    def generate_registro0110(self):
        cliente = self.cliente
        corretora = self.usuario

        # Registro 0000
        registro_0000 = (
            f"0000|{corretora.cnpj}|{corretora.nome_corretora}|{corretora.url or ''}|{corretora.endereco or ''}"
        )

        # Registro 0110
        valor_operacao_str = f"{self.valor_operacao or 0:.2f}".replace('.', ',')
        valor_taxas_str = f"{self.valor_taxas or 0:.2f}".replace('.', ',')
        quantidade_criptoativo_str = f"{self.quantidade_criptoativo or 0:.10f}".replace('.', ',')

        registro_0110 = (
            f"0110|{self.data_operacao.strftime('%d%m%Y')}|{self.numero_nota_fiscal or ''}|{self.codigo_operacao or ''}|"
            f"{valor_operacao_str}|{valor_taxas_str}|{self.simbolo_criptoativo or ''}|{quantidade_criptoativo_str}|"
            f"{self.hash_criptoativo or ''}|{cliente.tipo_ni or ''}|{cliente.pais or ''}|{cliente.cpf_cnpj or ''}|"
            f"{cliente.ni or ''}|{cliente.nome or ''}|{cliente.endereco or ''}|"
            f"{corretora.tipo_ni or ''}|{corretora.pais or ''}|{corretora.cnpj or ''}|{corretora.nome_corretora or ''}|{corretora.endereco or ''}"
        )

        # Registro 9999
        total_operacoes = 1  # Sempre será 1 para este caso específico
        total_valor_operacoes = f"{self.valor_operacao or 0:.2f}".replace('.', ',')
        total_taxas = f"{self.valor_taxas or 0:.2f}".replace('.', ',')

        registro_9999 = (
            f"9999|{total_operacoes}|{total_valor_operacoes}|{total_taxas}|"
            "0|0|0|0|0"
        )

        return f"{registro_0000}\n{registro_0110}\n{registro_9999}"

    def generate_and_save_file(self):
        directory = 'registros'
        if not os.path.exists(directory):
            os.makedirs(directory)
        
        filename = f"registro_{self.id}.txt"
        file_content = self.registro0110
        file_path = os.path.join(directory, filename)

        with open(file_path, 'w') as file:
            file.write(file_content)

        self.arquivo_registro.name = file_path
        super().save(update_fields=['arquivo_registro'])
