from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, Cliente
import re
from utils.cripto_data import tipos_ni, tipos_registro

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'password1', 'password2']

class UserEditForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    nome_corretora = forms.CharField(max_length=255, required=False)
    cnpj = forms.CharField(max_length=14, required=False)
    url = forms.URLField(max_length=200, required=False)
    endereco = forms.CharField(max_length=120, required=False)
    pais = forms.CharField(max_length=2, required=False)
    tipo_ni = forms.ChoiceField(choices=[(k, v) for k, v in tipos_ni.items()], required=False)
    tipo_de_registro = forms.ChoiceField(choices=[(k, v) for k, v in tipos_registro.items()], required=False)

    class Meta:
        model = CustomUser
        fields = ['email', 'nome_corretora', 'cnpj', 'url', 'endereco', 'pais', 'tipo_ni', 'tipo_de_registro']

    def clean_cnpj(self):
        cnpj = self.cleaned_data.get('cnpj')
        if cnpj:
            cnpj = re.sub(r'\D', '', cnpj)
            if len(cnpj) != 14:
                raise forms.ValidationError("CNPJ deve ter 14 dígitos.")
        return cnpj

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['cpf_cnpj', 'nome', 'endereco', 'pais', 'ni']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(ClienteForm, self).__init__(*args, **kwargs)
        if self.user:
            self.fields['corretora'] = forms.ModelChoiceField(
                queryset=Cliente.objects.filter(corretora=self.user), required=False)
            self.fields['corretora'].widget = forms.HiddenInput()
            self.fields['corretora'].initial = self.user
