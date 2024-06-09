from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
import re
from utils.cripto_data import tipos_ni, tipos_registro
from django.core.validators import RegexValidator

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('O email deve ser fornecido')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True, help_text="Email usado para login e comunicação.")
    nome_corretora = models.CharField(max_length=255, null=True, blank=True, help_text="Nome completo da corretora, pode conter caracteres especiais e espaços.")
    cnpj = models.CharField(max_length=14, unique=True, null=True, blank=True, help_text="CNPJ da corretora, usado para identificação fiscal. Apenas números são permitidos.")
    url = models.URLField(max_length=200, null=True, blank=True, help_text="URL do site da corretora.")
    endereco = models.CharField(max_length=120, null=True, blank=True, help_text="Endereço físico da corretora.")
    pais = models.CharField(max_length=2, null=True, blank=True, help_text="Sigla do país de operação da corretora.")
    tipo_ni = models.CharField(max_length=1, choices=[(k, v) for k, v in tipos_ni.items()], default='2', help_text="Tipo de NI da corretora (2 para CNPJ).")
    tipo_de_registro = models.CharField(max_length=4, choices=[(k, v) for k, v in tipos_registro.items()], default='0000', help_text="Tipo de registro.")

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def save(self, *args, **kwargs):
        if self.pais:
            self.pais = self.pais.upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email

    def get_registro_0000(self):
        tipo_de_registro = "0000"
        cnpj = self.cnpj or ""
        exchange_nome = self.nome_corretora or ""
        exchange_url = self.url or ""
        
        # Garantir que o CNPJ tenha apenas números
        cnpj = re.sub(r'\D', '', cnpj)
        
        # Remover pipes dos campos para evitar problemas de formatação
        exchange_nome = exchange_nome.replace('|', '')
        exchange_url = exchange_url.replace('|', '')
        
        registro = f"{tipo_de_registro}|{cnpj}|{exchange_nome}|{exchange_url}\n"
        return registro

class Cliente(models.Model):
    corretora = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='clientes_criados_accounts')
    cpf_cnpj = models.CharField(max_length=20, help_text="CPF ou CNPJ do cliente.")  # CompradorCPFCNPJ:
    nome = models.CharField(max_length=80, help_text="Nome completo do cliente.")  # CompradorNome:
    tipo_ni = models.CharField(max_length=1, editable=False, help_text="Tipo de documento de identificação do cliente (1 para CPF, 2 para CNPJ, 3 para NIF Pessoa Física, 4 para NIF Pessoa Jurídica, 5 para Passaporte).")  # CompradorTipoNI:
    endereco = models.CharField(max_length=120, help_text="Endereço completo do cliente.")  # CompradorEndereco:
    pais = models.CharField(max_length=2, help_text="Sigla do país do cliente.")  # CompradorPais:
    ni = models.CharField(
        max_length=30, 
        blank=True, 
        null=True, 
        help_text="Número de identificação adicional do cliente (opcional).",
        validators=[RegexValidator(regex=r'^[A-Za-z0-9]*$', message="Somente letras e números são permitidos.")]
    )

    def save(self, *args, **kwargs):
        self.cpf_cnpj = re.sub(r'\D', '', self.cpf_cnpj)
        if len(self.cpf_cnpj) == 11:
            self.tipo_ni = '1'  # CPF
        elif len(self.cpf_cnpj) == 14:
            self.tipo_ni = '2'  # CNPJ
        else:
            if self.tipo_ni == '3' or self.tipo_ni == '4':
                if not self.ni:
                    raise ValueError("NIF é obrigatório para os tipos de NI 3 e 4.")
            elif self.tipo_ni == '5':
                if not re.match(r'^[A-Za-z0-9]{8}$', self.cpf_cnpj):
                    raise ValueError("Passaporte deve ter 8 dígitos alfanuméricos.")
            elif self.tipo_ni in ('6', '7'):
                pass  # NIF não é obrigatório, nenhuma validação adicional necessária
            else:
                raise ValueError("CPF deve ter 11 dígitos e CNPJ deve ter 14 dígitos.")
        if self.pais:
            self.pais = self.pais.upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nome
    
