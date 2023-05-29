from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Tienda,Producto, Motivo, Mensajeria,Inventario,Inventario_producto,Usuario,Solicitud,estadoSolicitud
from django.contrib.auth import authenticate, login, logout
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404

import requests
import matplotlib.pyplot as plt
import matplotlib.pyplot as pltt
import mpld3

# Create your views here.

# Home
def home(request):
    inv = Inventario.objects.all()
    inventario_id = request.GET.get('inventario_id')  # Obtener el ID del inventario seleccionado
    filtro = Inventario_producto.objects.filter(inventarioId_id=inventario_id)
    # Obtener los IDs de producto asociados al filtro
    producto_ids = filtro.values_list('productoId_id', flat=True)
    # Obtener los datos de producto filtrando por los IDs obtenidos
    datosproducto = Producto.objects.filter(idProducto__in=producto_ids)
    usuario = Usuario.objects.all()
    invpro = Inventario_producto.objects.all()
    producto = Producto.objects.all()
    selected_inventario_id = Inventario.objects.get(idInventario=inventario_id) if inventario_id else None
    return render(request, 'core/home.html', {'selected_inventario_id': selected_inventario_id, 'filtro': filtro, 'inv': inv, 'producto': datosproducto, 'us': usuario, 'in': invpro, 'producto': producto})

def producto(request):
    producto = Producto.objects.all
    contexto = {"pro": producto}
    return render(request, 'core/producto.html', contexto)

def stock(request):
    producto = Producto.objects.all()
    inventario = Inventario.objects.all()
    contexto = {"pro":producto,"inv":inventario}
    return render(request, 'core/stock.html',contexto)

def tiendas(request):
    tiendas = Tienda.objects.all
    contexto = {"tie": tiendas}
    return render(request, 'core/tiendas.html', contexto)

def crearProducto(request):
    return render(request, 'core/crearProducto.html')

def responderSolicitud(request):
    return render(request, 'core/responderSolicitud.html')

def crearTienda(request):
    return render(request, 'core/crearTienda.html')

def crearUsuario(request):
    inventario = Inventario.objects.all()
    return render(request, 'core/crearUsuario.html', {'inv':inventario})



def menu(request):
    #us = Prescripcion.objects.all()
    #cad = Caducar.objects.all()
    #mes = Mensajeria.objects.all()
    # WEB SERVICES GET
    #response = requests.get('http://127.0.0.1:8000/api/listamed')
    #respon = requests.get('http://127.0.0.1:8000/api/listamen')
    resp = requests.get('http://127.0.0.1:8000/api/listaeliminados')
    #hab = response.json()
    #mes = respon.json()
    proEliminados = resp.json()
    usuarios = Usuario.objects.all()
    inventario = Inventario.objects.all()
    solicitudes = Solicitud.objects.all().order_by('-fechaSolicitud') 
    estado= estadoSolicitud.objects.all()
    contexto = {"estado":estado,"cad": proEliminados, "usuarios":usuarios, "inventario":inventario,"sol":solicitudes}
    return render(request, 'core/menu.html', contexto)

# Registrar
def registrar_usuario(request):
    nombre = request.POST['nombre']
    apellido = request.POST['apellido']
    email = request.POST['email']
    inv = request.POST['inv']
    passw = request.POST.get('password')
    repassw = request.POST['confirmpassword']

    if passw == repassw:  # Verificar si las contraseñas son iguales
        User.objects.create_user(username=email, first_name=nombre, is_superuser=1, is_staff=0, is_active=1, email=email, password=passw)
        Usuario.objects.create(nombres=nombre, apellidos=apellido, email=email, inventarioId_id=inv)
        messages.success(request, 'Usuario creado exitosamente!')
        return redirect('menu')
    else:
        messages.error(request, 'Las contraseñas no coinciden.')
        return redirect('crearUsuario')

def registrar_producto(request):
    nom = request.POST['nombre']
    pre = request.POST['precio']
    des = request.POST['descripcion']
    if request.FILES.get('image') == None:
        imagen_m = 'imagenproducto.png'
    else:
        imagen_m = request.FILES['image']

    Producto.objects.create(nombre=nom, precio=pre, descripcion=des, imagen=imagen_m, )
    messages.success(request, 'El producto ' + nom + ' se registro existosamente!')
    return redirect('producto')

def registrar_tienda(request):
    nom = request.POST['nombre']
    dire = request.POST['direccion']
    if request.FILES.get('image') == None:
        imagen_m = 'imagenproducto.png'
    else:
        imagen_m = request.FILES['image']

    tienda = Tienda.objects.create(nombreTienda=nom, direccion=dire,imagenTienda = imagen_m)
    Inventario.objects.create(tienda=tienda, inventario=nom)
    messages.success(request, f'La tienda {nom} se registró exitosamente!')
    return redirect('tiendas')

def registrar_stock(request):
    inv = request.POST['inv']
    pro = request.POST['pro']
    sto = int(request.POST['stock'])  # Asegúrate de convertir el stock a un número entero

    try:
        # Verificar si ya existe una entrada en la base de datos con los mismos IDs
        inventario_producto = Inventario_producto.objects.get(inventarioId_id=inv, productoId_id=pro)
        inventario_producto.stock += sto  # Sumar el stock existente con el nuevo stock
        inventario_producto.save()
        messages.success(request, 'Se registró el stock existosamente!')
    except Inventario_producto.DoesNotExist:
        # No existe una entrada con los mismos IDs, crear una nueva
        Inventario_producto.objects.create(stock=sto, inventarioId_id=inv, productoId_id=pro)
        messages.success(request, 'Se registró el stock existosamente!')
    return redirect('home')

def solicitarProducto(request):
    nomPro = request.POST['producto']
    inventario = request.POST['inventario']
    estado = 1

    Solicitud.objects.create(productoSolicitado = nomPro, estadoSol_id = estado,inventarioId_id = inventario)
    messages.success(request, f'La solicitud de stock de {nomPro} se envio exitosamente!')
    return redirect('home')


# Eliminar
def motivo(request, id):
    productos = Producto.objects.get(idProducto=id)
    contexto = {"hab": productos, }
    return render(request, 'core/motivo.html', contexto)


def eliminar(request, id):
    hab = Producto.objects.get(idProducto=id)
    nom = request.POST['nombre']
    mot = request.POST['motivo']
    if mot == None:
        messages.error(request, 'Completar')
    else:
        Motivo.objects.create(codigo=hab.idProducto, productoEliminado=hab.nombre, motivo=mot)
        hab.delete()
        messages.success(request, 'El prodcuto ' + nom + ' fue eliminado por la siguiente razón: '+mot)
        return redirect('menu')


def pendiente(request, id):  # Mensajeria
    cod = Mensajeria.objects.get(idMen=id)
    med = Producto.objects.get(nombre=cod.medicamento)

    email = cod.email
    print(email)
    template = get_template('core/email.html')
    content = template.render({'men': cod})

    if int(med.stock) >= int(cod.cantidad):
        med.stock = int(med.stock) - int(cod.cantidad)
        med.save()

        messages.success(
            request, "Se envio un correo al paciente avisando la disponibilidad de " + med.nombre)
        msg = EmailMultiAlternatives(
            'Cesfam',
            '',
            settings.EMAIL_HOST_USER,
            [email])
        msg.attach_alternative(content, 'text/html')
        msg.send()
        cod.delete()
    else:
        cod.cantidad = int(cod.cantidad) - int(med.stock)
        if int(med.stock) == 0:
            None
        else:
            messages.success(
                request, "Se envio un correo al paciente avisando la existencia de algunas unidades de " + med.nombre)
            med.stock = 0
            cod.save()
            med.save()
            msg = EmailMultiAlternatives(
                'Cesfam',
                'Hola, te enviamos un correo con tu factura',
                settings.EMAIL_HOST_USER,
                [email])
            msg.attach_alternative(content, 'text/html')
            msg.send()

    return redirect('menu')


# Modificar producto

def modificar_producto(request, id):
    productos = Producto.objects.get(idProducto=id)
    contexto = {"hab": productos}
    return render(request, 'core/modificar_producto.html', contexto)

def modificar(request):
    idisbn = request.POST['id']
    nom = request.POST['nombre']
    pre = request.POST['precio']
    sto = request.POST['stock']
    des = request.POST['descripcion']

    producto = Producto.objects.get(idProducto=idisbn)
    producto.nombre = nom
    producto.precio = pre
    producto.stock = sto
    producto.descripcion = des
    if request.FILES.get('img') != None:
        producto.imagen = request.FILES['img']
    producto.save()
    messages.success(request, 'Producto actualizado exitosamente!')
    return redirect('menu')


def responderSolicitud(request, id):
    estado = Solicitud.objects.get(idSolicitud = id)
    contexto = {"est": estado}
    return render(request, 'core/responderSolicitud.html', contexto)

def respuesta(request):
    idSol = request.POST['idSol']
    res = request.POST['respuesta']
    sol = Solicitud.objects.get(idSolicitud=idSol)

    sol.respuesta = res
    sol.estadoSol_id = 2
    sol.save()
    messages.success(request, 'Se envio la respuesta')
    return redirect('menu')


def modificar_inventario(request, id):
    inventario = Inventario_producto.objects.get(id=id)
    contexto = {"hab": inventario}
    return render(request, 'core/modificar_inventario.html', contexto)

def modifiInventario(request):
    idisbn = request.POST['id']
    nom = request.POST['nombre']
    sto = request.POST['stock']

    inventario_prod = Inventario_producto.objects.get(id=idisbn)
    inventario_prod.nombre = nom
    inventario_prod.stock = sto
    inventario_prod.save()
    messages.success(request, 'Inventario actualizado exitosamente!')
    return redirect('home')

def asignarUbicacion(request):
    idisbn = request.POST['id']
    est = request.POST['estante']
    comp = request.POST['compartimiento']

    inventario_prod = Inventario_producto.objects.get(id=idisbn)
    inventario_prod.estante = est
    inventario_prod.compartimiento = comp
    inventario_prod.save()
    messages.success(request, 'Ubicacion actualizada exitosamente!')
    return redirect('home')

# LOGIN_________________________________________________________________________________________________

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Usuario Inactivo')
        else:
            messages.error(request, 'Usuario y/o contraseña incorrecta')
        return redirect('login')
    else:
        return render(request, 'login.html')

# LOGOUT

def logout_view(request):
    logout(request)
    return redirect('login')
