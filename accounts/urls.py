from django.urls import path
from .views import login_view, logout_view, dashboard, home, register_view, edit_profile, create_cliente, edit_cliente, delete_cliente, list_clientes

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
    path('', home, name='home'),
    path('register/', register_view, name='register'),
    path('accounts/edit_profile/', edit_profile, name='edit_profile'),
    path('clientes/create/', create_cliente, name='create_cliente'),
    path('clientes/edit/<int:cliente_id>/', edit_cliente, name='edit_cliente'),
    path('clientes/delete/<int:cliente_id>/', delete_cliente, name='delete_cliente'),
    path('clientes/', list_clientes, name='list_clientes'),
]
