from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from .forms import UserRegisterForm, UserEditForm, ClienteForm
from .models import CustomUser, Cliente
from .serializers import CustomUserSerializer, ClienteSerializer

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect(reverse('dashboard'))
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect(reverse('login'))

@login_required
def dashboard(request):
    return render(request, 'accounts/dashboard.html', {'user': request.user})

def home(request):
    return render(request, 'accounts/home.html')

def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('login'))
    else:
        form = UserRegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def edit_profile(request):
    user = request.user
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect(reverse('dashboard'))
    else:
        form = UserEditForm(instance=user)
    return render(request, 'accounts/edit_profile.html', {'form': form})

@login_required
def create_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST, user=request.user)
        if form.is_valid():
            cliente = form.save(commit=False)
            cliente.corretora = request.user
            cliente.save()
            return redirect('list_clientes')
    else:
        form = ClienteForm(user=request.user)
    return render(request, 'accounts/create_cliente.html', {'form': form})

@login_required
def edit_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id, corretora=request.user)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect(reverse('list_clientes'))
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'accounts/edit_cliente.html', {'form': form})

@login_required
def delete_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id, corretora=request.user)
    if request.method == 'POST':
        cliente.delete()
        return redirect(reverse('list_clientes'))
    return render(request, 'accounts/delete_cliente.html', {'cliente': cliente})

@login_required
def list_clientes(request):
    clientes = Cliente.objects.filter(corretora=request.user)
    return render(request, 'accounts/list_clientes.html', {'clientes': clientes})

class CustomUserViewSet(viewsets.ModelViewSet):
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Retorna apenas o usuário logado
        return CustomUser.objects.filter(id=self.request.user.id)

    def perform_update(self, serializer):
        if self.request.user != serializer.instance:
            raise PermissionDenied("Você não tem permissão para editar este usuário.")
        serializer.save()

class ClienteViewSet(viewsets.ModelViewSet):
    serializer_class = ClienteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Retorna apenas os clientes associados ao usuário logado
        return Cliente.objects.filter(corretora=self.request.user)

    def perform_create(self, serializer):
        serializer.save(corretora=self.request.user)

    def perform_update(self, serializer):
        if serializer.instance.corretora != self.request.user:
            raise PermissionDenied("Você não tem permissão para editar este cliente.")
        super().perform_update(serializer)

    def perform_destroy(self, instance):
        if instance.corretora != self.request.user:
            raise PermissionDenied("Você não tem permissão para deletar este cliente.")
        super().perform_destroy(instance)
