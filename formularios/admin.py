from django.contrib import admin
from .models import Cliente, OperacaoCompraVenda
from .forms import ClienteForm, OperacaoCompraVendaForm

class ClienteAdmin(admin.ModelAdmin):
    form = ClienteForm
    list_display = ('nome', 'cpf_cnpj', 'pais', 'corretora')
    search_fields = ('nome', 'cpf_cnpj', 'corretora__email')
    list_filter = ('pais', 'corretora')

class OperacaoCompraVendaAdmin(admin.ModelAdmin):
    form = OperacaoCompraVendaForm
    list_display = (
        'usuario', 'cliente', 'data_operacao', 'codigo_operacao', 
        'valor_operacao', 'valor_taxas', 'simbolo_criptoativo', 
        'quantidade_criptoativo', 'numero_nota_fiscal'
    )
    search_fields = ('usuario__email', 'cliente__nome', 'codigo_operacao', 'simbolo_criptoativo')
    list_filter = ('data_operacao', 'codigo_operacao', 'usuario', 'cliente')
    fieldsets = (
        (None, {
            'fields': ('usuario', 'cliente', 'data_operacao', 'codigo_operacao', 
                       'valor_operacao', 'valor_taxas', 'simbolo_criptoativo', 
                       'quantidade_criptoativo', 'numero_nota_fiscal', 'hash_criptoativo')
        }),
    )

admin.site.register(Cliente, ClienteAdmin)
admin.site.register(OperacaoCompraVenda, OperacaoCompraVendaAdmin)
