from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required


#Views
from .views import home, stock, producto, menuSolicitud,tiendas,asignarUbicacion,modifiInventario,modificar_inventario, respuesta, responderSolicitud,crearProducto, solicitarProducto ,crearTienda, crearUsuario, menu, eliminar, motivo, proveedor, modificar_producto, registrar_producto, registrar_tienda, registrar_stock, modificar, registrar_usuario
from .views import login_view, logout_view

urlpatterns = [
    # Iniciar sesion, cerrar sesion.
    path('',LoginView.as_view(template_name='core/index.html'),name="login"),
    path('sesion', login_view, name="sesion"),
    path('logout', logout_view, name="logout"),

    #Html
    path('home',login_required(home), name ='home'),
    path('producto', login_required(producto), name='producto'),
    path('tiendas', login_required(tiendas), name='tiendas'),
    path('menu', login_required(menu), name='menu'),
    path('menuSolicitud', login_required(menuSolicitud), name='menuSolicitud'),

    #formularios registros.
    path('responderSolicitud', login_required(responderSolicitud), name='responderSolicitud'),
    path('crearTienda', login_required(crearTienda), name='crearTienda'),
    path('crearProducto', login_required(crearProducto), name='crearProducto'),
    path('crearUsuario', login_required(crearUsuario), name='crearUsuario'),
    path('stock', login_required(stock), name='stock'),

    #metodo de registrar.
    path('registrar_producto', login_required(registrar_producto), name='registrar_producto'),
    path('registrar_tienda', login_required(registrar_tienda), name='registrar_tienda'),
    path('registrar_stock', login_required(registrar_stock), name='registrar_stock'),
    path('registrar_usuario', login_required(registrar_usuario), name='registrar_usuario'),
    path('solicitarProducto', login_required(solicitarProducto), name='solicitarProducto'),

    #metodo de eliminar.
    path('eliminarproducto/<id>', login_required(motivo), name='eliminarproducto'), #Menu
    path('eliminar/<id>', eliminar, name='eliminar'), #Motivo
    path('proveedor/<id>', proveedor, name='proveedor'),

    #Metodo de modificar.
    path('modificarProducto/<id>', login_required(modificar_producto), name='modificar_producto'),
    path('responderSolicitud/<id>', login_required(responderSolicitud), name='responderSolicitud'),
    path('modificar_inventario/<id>', login_required(modificar_inventario), name='modificar_inventario'),
    path('modifi', login_required(modificar), name='modificar'),
    path('respuesta', respuesta, name='respuesta'),
    path('modifiInventario', login_required(modifiInventario), name='modifiInventario'),
    path('asignarUbicacion', login_required(asignarUbicacion), name='asignarUbicacion'),
]