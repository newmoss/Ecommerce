from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required


#Views
from .views import home, producto, crearProducto, menu, motivo, eliminar, pendiente, modificar_producto, registrar_producto, modificar, registrarUsuario
from .views import login_view, logout_view

urlpatterns = [
    # Iniciar, crear usuarios_________________________________________________________________________
    path('',LoginView.as_view(template_name='core/1Logear.html'),name="login"),
    path('sesion', login_view, name="sesion"),
    path('logout', logout_view, name="logout"),

    path('home',login_required(home), name ='home'),
    path('producto', login_required(producto), name='producto'),
    path('crearProducto', login_required(crearProducto), name='crearProducto'),
    path('menu', login_required(menu), name='menu'),

    #metodo de registrar, eliminar y modificar.
    path('registrar_producto', login_required(registrar_producto), name='registrar_producto'),
    path('registrar', registrarUsuario, name='registrar'),

    path('eliminarproducto/<id>', login_required(motivo), name='eliminarproducto'), #Menu
    path('eliminar/<id>', eliminar, name='eliminar'), #Motivo

    path('pendiente/<id>', pendiente, name='pen'),

    path('modifi', login_required(modificar), name='modificar'),
    path('modificarProducto/<id>', login_required(modificar_producto), name='modificar_producto'),





]