from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FormularioViewSet, create_formulario, list_formularios, edit_formulario, delete_formulario
from .views import FormularioFinalViewSet, create_formulario_final, list_formularios_finais, edit_formulario_final, delete_formulario_final, download_formulario_final

router = DefaultRouter()
router.register(r'formularios', FormularioViewSet, basename='formulario')
router.register(r'formularios_finais', FormularioFinalViewSet, basename='formulariofinal')

urlpatterns = [
    path('formularios/', list_formularios, name='formulario_list'),
    path('formularios/create/', create_formulario, name='create_formulario'),
    path('formularios/edit/<int:pk>/', edit_formulario, name='edit_formulario'),
    path('formularios/delete/<int:pk>/', delete_formulario, name='delete_formulario'),
    path('formularios_finais/', list_formularios_finais, name='formulario_final_list'),
    path('formularios_finais/create/', create_formulario_final, name='create_formulario_final'),
    path('formularios_finais/edit/<int:pk>/', edit_formulario_final, name='edit_formulario_final'),
    path('formularios_finais/delete/<int:pk>/', delete_formulario_final, name='delete_formulario_final'),
    path('formularios_finais/download/<int:pk>/', download_formulario_final, name='download_formulario_final'),
]
