import hashlib
import os
from django.db import models
from django.conf import settings
from accounts.models import CustomUser, Cliente
from utils.cripto_data import tipos_ni, tipos_registro, codigos_operacao


class Formulario(models.Model):
    usuario = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    tipo_registro = models.CharField(max_length=4, choices=[(k, v) for k, v in tipos_registro.items()], help_text="Código do tipo de registro conforme tabela do manual.")
    data_operacao = models.DateField(help_text="Data da operação no formato DDMMAAAA.")  # OperacaoData
    codigo_operacao = models.CharField(max_length=4, choices=[(k, v) for k, v in codigos_operacao.items()], help_text="Código da operação conforme tabela de código.")
    valor_operacao = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True, help_text="Valor da operação em reais excluídas as taxas.")  # OperacaoValor:
    valor_taxas = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, help_text="Valor das taxas em reais cobradas na operação.")  # OperacaoTaxasValor
    simbolo_criptoativo = models.CharField(max_length=10, blank=True, null=True, help_text="Símbolo do criptoativo. Ex: BTC para bitcoin, ETH para Ethereum, etc.")  # CriptoativoSimbolo
    quantidade_criptoativo = models.DecimalField(max_digits=26, decimal_places=10, blank=True, null=True, help_text="Quantidade de criptoativos comprados.")  # CriptoativoQuantidade:
    numero_nota_fiscal = models.CharField(max_length=30, blank=True, null=True, help_text="Número da nota fiscal da operação.")  # OperacaoID:
    hash_criptoativo = models.TextField(blank=True, null=True, help_text="Hash do criptoativo.")
    registro = models.TextField(blank=True, null=True, editable=False, help_text="Campo preenchido automaticamente pelo sistema.")

    def __str__(self):
        return f"{self.tipo_registro} - {self.codigo_operacao} - {self.data_operacao}"

    def save(self, *args, **kwargs):
        if self.tipo_registro == '0110':
            self.codigo_operacao = 'I'
            self.automatizar_campos_0110()
        elif self.tipo_registro == '0210':
            self.codigo_operacao = 'II'
            self.automatizar_campos_0210()
        elif self.tipo_registro == '0410':
            self.codigo_operacao = 'IV'
            self.automatizar_campos_0410()
        elif self.tipo_registro == '0510':
            self.codigo_operacao = 'V'
            self.automatizar_campos_0510()
        elif self.tipo_registro == '0710':
            self.codigo_operacao = 'VII'
            self.automatizar_campos_0710()
        if not self.id:  # Se for uma nova instância
            self.registro = self.generate_registro()
        super().save(*args, **kwargs)

    def automatizar_campos_0110(self):
        if not self.numero_nota_fiscal:
            self.numero_nota_fiscal = self.gerar_numero_nota_fiscal()
        if not self.valor_taxas:
            self.valor_taxas = 0.00
        if not self.hash_criptoativo:
            self.hash_criptoativo = self.gerar_hash_criptoativo()

    def automatizar_campos_0210(self):
        if not self.numero_nota_fiscal:
            self.numero_nota_fiscal = self.gerar_numero_nota_fiscal()
        if not self.valor_taxas:
            self.valor_taxas = 0.00
        if not self.hash_criptoativo:
            self.hash_criptoativo = self.gerar_hash_criptoativo()

    def automatizar_campos_0410(self):
        if not self.numero_nota_fiscal:
            self.numero_nota_fiscal = self.gerar_numero_nota_fiscal()
        if not self.valor_taxas:
            self.valor_taxas = 0.00
        if not self.hash_criptoativo:
            self.hash_criptoativo = self.gerar_hash_criptoativo()

    def automatizar_campos_0510(self):
        if not self.numero_nota_fiscal:
            self.numero_nota_fiscal = self.gerar_numero_nota_fiscal()
        if not self.valor_taxas:
            self.valor_taxas = 0.00
        if not self.hash_criptoativo:
            self.hash_criptoativo = self.gerar_hash_criptoativo()

    def automatizar_campos_0710(self):
        if not self.numero_nota_fiscal:
            self.numero_nota_fiscal = self.gerar_numero_nota_fiscal()
        if not self.valor_taxas:
            self.valor_taxas = 0.00
        if not self.hash_criptoativo:
            self.hash_criptoativo = self.gerar_hash_criptoativo()

    def gerar_numero_nota_fiscal(self):
        return f"NF-{self.data_operacao.strftime('%Y%m%d')}-{self.cliente.id}"

    def gerar_hash_criptoativo(self):
        hash_input = f"{self.simbolo_criptoativo}{self.quantidade_criptoativo}{self.data_operacao}".encode('utf-8')
        return hashlib.sha256(hash_input).hexdigest()

    def sanitize_field(self, field_value):
        if field_value:
            return field_value.replace('|', '')
        return field_value

    def generate_registro(self):
        cliente = self.cliente
        corretora = self.usuario

        valor_operacao_str = f"{self.valor_operacao or 0:.2f}".replace('.', ',')
        valor_taxas_str = f"{self.valor_taxas or 0:.2f}".replace('.', ',')
        quantidade_criptoativo_str = f"{self.quantidade_criptoativo or 0:.10f}".replace('.', ',')

        # Sanitizar campos para remover pipes
        sanitized_fields = {
            "numero_nota_fiscal": self.sanitize_field(self.numero_nota_fiscal),
            "codigo_operacao": self.sanitize_field(self.codigo_operacao),
            "simbolo_criptoativo": self.sanitize_field(self.simbolo_criptoativo),
            "hash_criptoativo": self.sanitize_field(self.hash_criptoativo),
            "cliente_nome": self.sanitize_field(cliente.nome),
            "cliente_endereco": self.sanitize_field(cliente.endereco),
            "corretora_nome": self.sanitize_field(corretora.nome_corretora),
            "corretora_endereco": self.sanitize_field(corretora.endereco),
        }

        registro = (
            f"{self.tipo_registro}|{self.data_operacao.strftime('%d%m%Y')}|{sanitized_fields['numero_nota_fiscal'] or ''}|{sanitized_fields['codigo_operacao'] or ''}|"
            f"{valor_operacao_str}|{valor_taxas_str}|{sanitized_fields['simbolo_criptoativo'] or ''}|{quantidade_criptoativo_str}|"
            f"{sanitized_fields['hash_criptoativo'] or ''}|{cliente.tipo_ni or ''}|{cliente.pais or ''}|{cliente.cpf_cnpj or ''}|{cliente.ni or ''}|"
            f"{sanitized_fields['cliente_nome'] or ''}|{sanitized_fields['cliente_endereco'] or ''}|"
            f"{corretora.tipo_ni or ''}|{corretora.pais or ''}|{corretora.cnpj or ''}|{sanitized_fields['corretora_nome'] or ''}|{sanitized_fields['corretora_endereco'] or ''}"
        )

        return registro
    

class FormularioFinal(models.Model):
    usuario = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    data_inicial = models.DateField()
    data_final = models.DateField()
    arquivo_final = models.FileField(upload_to='arquivos_finais/', blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.id:  # Se for uma nova instância
            super().save(*args, **kwargs)  # Salva para ter um ID
            self.arquivo_final = self.gerar_arquivo_final()
        super().save(*args, **kwargs)

    def gerar_arquivo_final(self):
        formularios = Formulario.objects.filter(usuario=self.usuario, data_operacao__range=[self.data_inicial, self.data_final])

        registros = []

        # Registro 0000
        registro_0000 = self.gerar_registro_0000()
        registros.append(registro_0000)

        # Outros registros
        for formulario in formularios:
            registros.append(formulario.registro)

        # Registro 9999
        registro_9999 = self.gerar_registro_9999(formularios)
        registros.append(registro_9999)

        # Unir todos os registros em um único texto
        arquivo_final_content = '\n'.join(registros) + '\n'

        # Definir o caminho do arquivo
        filename = f'formulario_final_{self.usuario.id}_{self.data_inicial}_{self.data_final}.txt'
        filepath = os.path.join(settings.MEDIA_ROOT, 'arquivos_finais', filename)

        # Criar diretório se não existir
        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        # Salvar o conteúdo no arquivo
        with open(filepath, 'w', encoding='utf-8') as file:
            file.write(arquivo_final_content)

        # Definir o caminho do arquivo no campo FileField
        self.arquivo_final.name = os.path.join('arquivos_finais', filename)
        return self.arquivo_final.name

    def gerar_registro_0000(self):
        usuario = self.usuario
        registro = f"0000|{usuario.cnpj}|{usuario.nome_corretora}|{usuario.url}|"
        return registro

    def gerar_registro_9999(self, formularios):
        tipo_registro_count = {
            '0110': 0,
            '0210': 0,
            '0410': 0,
            '0510': 0,
            '0710': 0,
            '0910': 0,
            '1000': 0,
            '1010': 0,
        }

        tipo_registro_total = {
            '0110': 0.00,
            '0210': 0.00,
            '0410': 0.00,
            '0510': 0.00,
            '0710': 0.00,
            '0910': 0.00,
            '1000': 0.00,
            '1010': 0.00,
        }

        for formulario in formularios:
            tipo_registro_count[formulario.tipo_registro] += 1
            tipo_registro_total[formulario.tipo_registro] += float(formulario.valor_operacao or 0)

        registro = (
            f"9999|{tipo_registro_count['0110']}|{tipo_registro_total['0110']:.2f}|{tipo_registro_count['0210']}|"
            f"{tipo_registro_total['0210']:.2f}|{tipo_registro_count['0410']}|{tipo_registro_total['0410']:.2f}|"
            f"{tipo_registro_count['0510']}|{tipo_registro_total['0510']:.2f}|{tipo_registro_count['0710']}|"
            f"{tipo_registro_total['0710']:.2f}|{tipo_registro_count['0910']}|{tipo_registro_total['0910']:.2f}|"
            f"{tipo_registro_count['1000']}|{tipo_registro_total['1000']:.2f}|{tipo_registro_count['1010']}|"
            f"{tipo_registro_total['1010']:.2f}|"
        )
        return registro