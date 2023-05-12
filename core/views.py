from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Tienda,Producto, Motivo, Mensajeria,Inventario,Inventario_producto
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
    #productos = Producto.objects.all()
    #
    #nombres = [producto.nombre for producto in productos]
    #precios = [producto.precio for producto in productos]
    #plt.bar(range(len(nombres)), precios)
    #plt.xlabel('Productos')
    #plt.ylabel('Precios')
    #plt.title('Gráfico de precios de productos')
    #
    ## Establecer los nombres de los productos como etiquetas en el eje x
    #plt.xticks(range(len(nombres)), nombres, rotation=90)
#
    #html_graph = mpld3.fig_to_html(plt.gcf())
    inv = Inventario.objects.all()
    inventario_id = request.GET.get('inventario_id')  # Obtener el ID del inventario seleccionado

    # Obtener el inventario correspondiente al ID proporcionado
    # Obtener los productos relacionados con el inventario seleccionado
    filtro = Inventario_producto.objects.filter(inventarioId_id=inventario_id)

    # Obtener los IDs de producto asociados al filtro
    producto_ids = filtro.values_list('productoId_id', flat=True)

    # Obtener los datos de producto filtrando por los IDs obtenidos
    datosproducto = Producto.objects.filter(idProducto__in=producto_ids)

    return render(request, 'core/home.html', {'filtro': filtro, 'inv': inv, 'producto':datosproducto})



def producto(request):
    hab = Producto.objects.all
    contexto = {"hab": hab}
    return render(request, 'core/producto.html', contexto)

def tiendas(request):
    hab = Tienda.objects.all
    contexto = {"hab": hab}
    return render(request, 'core/tiendas.html', contexto)


def crearProducto(request):
    return render(request, 'core/crearProducto.html')

def crearTienda(request):
    return render(request, 'core/crearTienda.html')

def stock(request):
    pro = Producto.objects.all()
    inv = Inventario.objects.all()
    contexto = {"pro":pro,"inv":inv}
    return render(request, 'core/stock.html',contexto)

def mostrar_productos(request):
    inv = Inventario.objects.all()
    inventario_id = request.GET.get('inventario_id')  # Obtener el ID del inventario seleccionado

    # Obtener el inventario correspondiente al ID proporcionado
    # Obtener los productos relacionados con el inventario seleccionado
    filtro = Inventario_producto.objects.filter(inventarioId_id=inventario_id)

    # Obtener los IDs de producto asociados al filtro
    producto_ids = filtro.values_list('productoId_id', flat=True)

    # Obtener los datos de producto filtrando por los IDs obtenidos
    datosproducto = Producto.objects.filter(idProducto__in=producto_ids)

    return render(request, 'core/mostrarinv.html', {'filtro': filtro, 'inv': inv, 'producto':datosproducto})


def menu(request):
    #us = Prescripcion.objects.all()
    #cad = Caducar.objects.all()
    #mes = Mensajeria.objects.all()
    hab = Producto.objects.all()

    # WEB SERVICES GET
    #response = requests.get('http://127.0.0.1:8000/api/listamed')
    respon = requests.get('http://127.0.0.1:8000/api/listamen')
    resp = requests.get('http://127.0.0.1:8000/api/listaeliminados')

    #hab = response.json()
    mes = respon.json()
    cad = resp.json()

    contexto = {"hab": hab, "cad": cad, "mes": mes}
    return render(request, 'core/menu.html', contexto)


# Registrar
def registrarUsuario(request):
    nombres = request.POST['nombres']
    email = request.POST['email']
    password = request.POST['password1']
    print(nombres,email,password)
    if nombres and email and password:
        User.objects.create_user(username=nombres, first_name=nombres, is_staff=0, is_active=1, email=email, password=make_password(password))
        messages.success(request, 'Usuario creado exitosamente!')
        return redirect('home')
    else:
        messages.error(request, 'Error al crear el usuario. Por favor, completa todos los campos.')
        return redirect('login')


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

    Tienda.objects.create(nombreTienda=nom,direccion=dire)
    tienda = Tienda.objects.all()
    Inventario.objects.create(tienda_id = tienda.idTienda)

    messages.success(request, 'La tienda' + nom + ' se registro existosamente!')
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




# Eliminar
def motivo(request, id):
    hab = Producto.objects.get(idProducto=id)
    contexto = {"hab": hab, }
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
        messages.success(request, 'El medicamento ' + nom + ' fue caducado por la siguiente razón: '+mot)
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
    hab = Producto.objects.get(idProducto=id)
    contexto = {"hab": hab, }
    return render(request, 'core/modificar_producto.html', contexto)


def modificar(request):
    idisbn = request.POST['id']
    nom = request.POST['nombre']
    pre = request.POST['precio']
    sto = request.POST['stock']
    des = request.POST['descripcion']

    hab = Producto.objects.get(idProducto=idisbn)

    hab.nombre = nom
    hab.precio = pre
    hab.stock = sto
    hab.descripcion = des

    if request.FILES.get('img') != None:
        hab.imagen = request.FILES['img']
    hab.save()
    messages.success(request, 'Producto actualizado exitosamente!')
    return redirect('menu')

# LOGIN_________________________________________________________________________________________________

def login_view(request):
    u = request.POST['username']
    c = request.POST['password']
    print(u)
    print(c)
    user = authenticate(username=u, password=c)

    if user is not None:
        if user.is_active:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Usuario Inactivo')
    else:
        messages.error(request, 'Usuario y/o contraseña incorrecta')
    return redirect('login')

# LOGOUT

def logout_view(request):
    logout(request)
    return redirect('login')
