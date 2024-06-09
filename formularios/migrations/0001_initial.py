# Generated by Django 5.0.6 on 2024-06-07 10:30

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cpf_cnpj', models.CharField(help_text='CPF ou CNPJ do cliente.', max_length=20)),
                ('nome', models.CharField(help_text='Nome completo do cliente.', max_length=80)),
                ('tipo_ni', models.CharField(editable=False, help_text='Tipo de documento de identificação do cliente (1 para CPF, 2 para CNPJ).', max_length=1)),
                ('endereco', models.CharField(help_text='Endereço completo do cliente.', max_length=120)),
                ('pais', models.CharField(help_text='Sigla do país do cliente.', max_length=2)),
                ('corretora', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='clientes_criados', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OperacaoCompraVenda',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_registro', models.CharField(default='0110', editable=False, help_text='Texto fixo contendo a identificação do registro (0110).', max_length=4)),
                ('data_operacao', models.DateField(help_text='Data da operação no formato DDMMAAAA.')),
                ('codigo_operacao', models.CharField(default='I', help_text='Código da operação conforme tabela de código (I para compra e venda).', max_length=4)),
                ('valor_operacao', models.DecimalField(decimal_places=2, help_text='Valor da operação em reais excluídas as taxas.', max_digits=15)),
                ('valor_taxas', models.DecimalField(blank=True, decimal_places=2, help_text='Valor das taxas em reais cobradas na operação.', max_digits=10, null=True)),
                ('simbolo_criptoativo', models.CharField(help_text='Símbolo do criptoativo. Ex: BTC para bitcoin, ETH para Ethereum, etc.', max_length=10)),
                ('quantidade_criptoativo', models.DecimalField(decimal_places=10, help_text='Quantidade de criptoativos comprados.', max_digits=26)),
                ('numero_nota_fiscal', models.CharField(help_text='Número da nota fiscal da operação.', max_length=30)),
                ('hash_criptoativo', models.TextField(blank=True, help_text='Hash do criptoativo.', null=True)),
                ('registro0110', models.TextField(blank=True, editable=False, help_text='Campo preenchido automaticamente pelo sistema.', null=True)),
                ('arquivo_registro', models.FileField(blank=True, help_text='Arquivo de registro gerado automaticamente.', null=True, upload_to='registros/')),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='formularios.cliente')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
