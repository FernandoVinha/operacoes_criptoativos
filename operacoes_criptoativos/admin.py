from django.contrib import admin
from .models import Formulario, FormularioFinal

@admin.register(Formulario)
class FormularioAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'cliente', 'tipo_registro', 'data_operacao', 'codigo_operacao')
    search_fields = ('tipo_registro', 'codigo_operacao', 'usuario__email', 'cliente__nome')
    list_filter = ('tipo_registro', 'data_operacao')
    readonly_fields = ('registro',)
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(usuario=request.user)

    def save_model(self, request, obj, form, change):
        if not obj.pk:  # Adiciona o usuário logado na criação
            obj.usuario = request.user
        super().save_model(request, obj, form, change)

@admin.register(FormularioFinal)
class FormularioFinalAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'data_inicial', 'data_final', 'arquivo_final')
    search_fields = ('usuario__email', 'data_inicial', 'data_final')
    list_filter = ('data_inicial', 'data_final')
    readonly_fields = ('arquivo_final',)
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(usuario=request.user)

    def save_model(self, request, obj, form, change):
        if not obj.pk:  # Adiciona o usuário logado na criação
            obj.usuario = request.user
        super().save_model(request, obj, form, change)
