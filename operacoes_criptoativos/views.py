from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Formulario, FormularioFinal
from .forms import FormularioForm, FormularioFinalForm
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from .serializers import FormularioSerializer, FormularioFinalSerializer
import os

@login_required
def create_formulario(request):
    if request.method == 'POST':
        form = FormularioForm(request.POST, user=request.user)
        if form.is_valid():
            formulario = form.save(commit=False)
            formulario.usuario = request.user
            formulario.save()
            return redirect('formulario_list')
    else:
        form = FormularioForm(user=request.user)
    return render(request, 'operacoes_criptoativos/formulario_form.html', {'form': form})

@login_required
def edit_formulario(request, pk):
    formulario = get_object_or_404(Formulario, pk=pk, usuario=request.user)
    if request.method == 'POST':
        form = FormularioForm(request.POST, instance=formulario, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('formulario_list')
    else:
        form = FormularioForm(instance=formulario, user=request.user)
    return render(request, 'operacoes_criptoativos/formulario_form.html', {'form': form})

@login_required
def delete_formulario(request, pk):
    formulario = get_object_or_404(Formulario, pk=pk, usuario=request.user)
    if request.method == 'POST':
        formulario.delete()
        return redirect('formulario_list')
    return render(request, 'operacoes_criptoativos/formulario_confirm_delete.html', {'formulario': formulario})

@login_required
def list_formularios(request):
    formularios = Formulario.objects.filter(usuario=request.user)
    return render(request, 'operacoes_criptoativos/formulario_list.html', {'formularios': formularios})

class FormularioViewSet(viewsets.ModelViewSet):
    serializer_class = FormularioSerializer
    permission_classes = [IsAuthenticated]
    queryset = Formulario.objects.all()

    def get_queryset(self):
        return Formulario.objects.filter(usuario=self.request.user)

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)

    def perform_update(self, serializer):
        if serializer.instance.usuario != self.request.user:
            raise PermissionDenied("Você não tem permissão para editar este formulário.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.usuario != self.request.user:
            raise PermissionDenied("Você não tem permissão para deletar este formulário.")
        instance.delete()

#_________________________ Formulário Final _________________________

@login_required
def create_formulario_final(request):
    if request.method == 'POST':
        form = FormularioFinalForm(request.POST)
        if form.is_valid():
            formulario_final = form.save(commit=False)
            formulario_final.usuario = request.user
            formulario_final.save()
            return redirect('formulario_final_list')
    else:
        form = FormularioFinalForm()
    return render(request, 'operacoes_criptoativos/formulario_final_form.html', {'form': form})

@login_required
def edit_formulario_final(request, pk):
    formulario_final = get_object_or_404(FormularioFinal, pk=pk, usuario=request.user)
    if request.method == 'POST':
        form = FormularioFinalForm(request.POST, instance=formulario_final)
        if form.is_valid():
            form.save()
            return redirect('formulario_final_list')
    else:
        form = FormularioFinalForm(instance=formulario_final)
    return render(request, 'operacoes_criptoativos/formulario_final_form.html', {'form': form})

@login_required
def delete_formulario_final(request, pk):
    formulario_final = get_object_or_404(FormularioFinal, pk=pk, usuario=request.user)
    if request.method == 'POST':
        formulario_final.delete()
        return redirect('formulario_final_list')
    return render(request, 'operacoes_criptoativos/formulario_final_confirm_delete.html', {'formulario_final': formulario_final})

@login_required
def list_formularios_finais(request):
    formularios_finais = FormularioFinal.objects.filter(usuario=request.user)
    return render(request, 'operacoes_criptoativos/formulario_final_list.html', {'formularios_finais': formularios_finais})

@login_required
def download_formulario_final(request, pk):
    formulario_final = get_object_or_404(FormularioFinal, pk=pk, usuario=request.user)
    filepath = formulario_final.arquivo_final.path

    # Adicionar CR e LF ao final de cada linha
    corrected_content = []
    with open(filepath, 'r') as f:
        for line in f:
            corrected_content.append(line.strip() + '\r\n')
    
    response = HttpResponse(''.join(corrected_content), content_type='application/text')
    response['Content-Disposition'] = f'attachment; filename={os.path.basename(filepath)}'
    return response

class FormularioFinalViewSet(viewsets.ModelViewSet):
    serializer_class = FormularioFinalSerializer
    permission_classes = [IsAuthenticated]
    queryset = FormularioFinal.objects.all()

    def get_queryset(self):
        return FormularioFinal.objects.filter(usuario(self.request.user)

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)

    def perform_update(self, serializer):
        if serializer.instance.usuario != self.request.user:
            raise PermissionDenied("Você não tem permissão para editar este formulário.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.usuario != self.request.user:
            raise PermissionDenied("Você não tem permissão para deletar este formulário.")
        instance.delete()
