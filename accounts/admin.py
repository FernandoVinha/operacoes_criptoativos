from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Cliente
from .forms import UserRegisterForm, UserEditForm, ClienteForm

class CustomUserAdmin(UserAdmin):
    add_form = UserRegisterForm
    form = UserEditForm
    model = CustomUser
    list_display = ('email', 'nome_corretora', 'cnpj', 'url', 'endereco', 'pais', 'tipo_ni', 'tipo_de_registro', 'is_staff', 'is_active', 'registro')
    list_filter = ('is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Informações Pessoais', {'fields': ('nome_corretora', 'cnpj', 'url', 'endereco', 'pais', 'tipo_ni', 'tipo_de_registro')}),
        ('Permissões', {'fields': ('is_staff', 'is_active', 'groups', 'user_permissions')}),
        ('Datas Importantes', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active', 'groups', 'user_permissions')}
        ),
    )
    search_fields = ('email', 'nome_corretora', 'cnpj')
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions',)

    def registro(self, obj):
        return obj.get_registro_0000()
    registro.short_description = 'Registro 0000'

admin.site.register(CustomUser, CustomUserAdmin)

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    form = ClienteForm
    list_display = ('corretora', 'nome', 'cpf_cnpj', 'tipo_ni', 'corretora', 'endereco', 'pais')
    search_fields = ('nome', 'cpf_cnpj')
    list_filter = ('cpf_cnpj', 'corretora')
