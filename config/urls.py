from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from accounts.views import CustomUserViewSet, ClienteViewSet
from operacoes_criptoativos.views import FormularioViewSet

# Cria o roteador e registra as views
router = DefaultRouter()
router.register(r'users', CustomUserViewSet, basename='user')
router.register(r'clientes', ClienteViewSet, basename='cliente')
router.register(r'formularios', FormularioViewSet, basename='formulario')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('operacoes_criptoativos/', include('operacoes_criptoativos.urls')),
    path('api/', include(router.urls)),  # Inclui todas as rotas de API em um único ponto de entrada
]
