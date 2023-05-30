from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Tienda,Producto, Motivo, Mensajeria, Inventario, Inventario_producto, Usuario, Solicitud, estadoSolicitud
from django.contrib.auth import authenticate, login, logout
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.conf import settings
from django.contrib.auth.models import User
import requests

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
    producto = Producto.objects.all().exclude(stockProducto =0)
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
    # WEB SERVICES GET
    #response = requests.get('http://127.0.0.1:8000/api/listamed')
    #respon = requests.get('http://127.0.0.1:8000/api/listamen')    
    # #hab = response.json()
    #mes = respon.json()
    resp = requests.get('http://127.0.0.1:8000/api/listaeliminados')
    productosEliminados = resp.json()
    usuarios = Usuario.objects.all()
    inventario = Inventario.objects.all()
    solicitudes = Solicitud.objects.all().order_by('-fechaSolicitud') 
    estado= estadoSolicitud.objects.all()
    contexto = {"estado":estado,"cad": productosEliminados, "usuarios":usuarios, "inventario":inventario,"sol":solicitudes}
    return render(request, 'core/menu.html', contexto)

# Registrar los datos en BD
def registrar_usuario(request):
    nombre = request.POST['nombre']
    apellido = request.POST['apellido']
    email = request.POST['email']
    inventario = request.POST['inv']
    passw = request.POST.get('password')
    repassw = request.POST['confirmpassword']

    try:
        # Verificar si el email ya existe en la tabla User
        User.objects.get(email=email)
        messages.error(request, {
            'title': 'Error',
            'text': 'Este correo ya está registrado.',
            'icon': 'error'
        })
        return redirect('crearUsuario')
    except User.DoesNotExist:
        try:
            # Verificar si el email ya existe en la tabla Usuario
            Usuario.objects.get(email=email)
            messages.error(request, {
                'title': 'Error',
                'text': 'Este correo ya está registrado.',
                'icon': 'error'
            })
            return redirect('crearUsuario')
        except Usuario.DoesNotExist:
            if passw == repassw:  # Verificar si las contraseñas son iguales
                User.objects.create_user(username=email, first_name=nombre, is_superuser=1, is_staff=0, is_active=1, email=email, password=passw)
                Usuario.objects.create(nombres=nombre, apellidos=apellido, email=email, inventarioId_id=inventario)
                messages.success(request, {
                    'title': 'Cuenta creada',
                    'text': 'Usuario creado exitosamente!',
                    'icon': 'info'
                })
                return redirect('menu')
            else:
                messages.error(request, {
                    'title': 'Error',
                    'text': 'Las contraseñas no coinciden.',
                    'icon': 'error'
                })
                return redirect('crearUsuario')

def registrar_producto(request):
    nom = request.POST['nombre']
    pre = request.POST['precio']
    sto = request.POST['stock']

    des = request.POST['descripcion']
    if request.FILES.get('image') == None:
        imagen_m = 'imagenproducto.png'
    else:
        imagen_m = request.FILES['image']
    Producto.objects.create(nombre=nom, precio=pre, descripcion=des, stockProducto = sto, imagen=imagen_m, )
    messages.success(request, {
                    'title': 'Producto registrado',
                    'text': 'El producto ' + nom + ' se registro existosamente!',
                    'icon': 'success'
                })
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
    messages.success(request, {'title': 'Producto registrado',
                    'text': 'La tienda ' + nom +' se registró exitosamente!',
                    'icon': 'success'})
    return redirect('tiendas')

def registrar_stock(request):
    inventario = request.POST['inv']
    producto = request.POST['pro']
    stock = int(request.POST['stock'])  # Asegúrate de convertir el stock a un número entero

    try:
        # Verificar si ya existe una entrada en la base de datos con los mismos IDs
        inventario_producto = Inventario_producto.objects.get(inventarioId_id=inventario, productoId_id=producto)
        producto = Producto.objects.get(idProducto=producto)
        stock_original = producto.stockProducto
        if stock <= stock_original:
            inventario_producto.stock += stock  # Sumar el stock existente con el nuevo stock
            inventario_producto.save()
            producto.stockProducto -= stock
            producto.save()
            messages.success(request, {
                    'title': 'Actualizacion de stock',
                    'text': 'El producto ya existe en el inventario, actualizamos el stock',
                    'icon': 'info'})
            return redirect('menu')
        else:
            messages.error(request, {
                    'title': 'Cuidado',
                    'text': 'El stock a registrar es mayor al stock disponible.',
                    'icon': 'warning'})
            return redirect('stock')
    except Inventario_producto.DoesNotExist:
        # No existe una entrada con los mismos IDs, crear una nueva
        Inventario_producto.objects.create(stock=stock, inventarioId_id=inventario, productoId_id=producto)
        messages.success(request, {
                    'title': 'Producto registrado',
                    'text': 'Se registró el producto exitosamente!',
                    'icon': 'success'})
    return redirect('home')

def solicitarProducto(request):
    nomProducto = request.POST['producto']
    inventario = request.POST['inventario']
    estado = 1
    Solicitud.objects.create(productoSolicitado = nomProducto, estadoSol_id = estado,inventarioId_id = inventario)
    messages.success(request,{
                    'title': 'Solicitud enviada',
                    'text': f'La solicitud de stock de {nomProducto} se envio exitosamente!',
                    'icon': 'success'})
    return redirect('home')

# Vista Eliminar
def motivo(request, id):
    productos = Producto.objects.get(idProducto=id)
    contexto = {"hab": productos, }
    return render(request, 'core/motivo.html', contexto)

# Funcion de eliminar
def eliminar(request, id):
    hab = Producto.objects.get(idProducto=id)
    nom = request.POST['nombre']
    mot = request.POST['motivo']
    if mot == None:
        messages.error(request,{
                    'title': 'Incompleto',
                    'text': 'Completa el formulario correctamente',
                    'icon': 'warning'})
    else:
        Motivo.objects.create(codigo=hab.idProducto, productoEliminado=hab.nombre, motivo=mot)
        hab.delete()
        messages.success(request,{
                    'title': 'Producto eliminado',
                    'text': 'El producto '+nom+' fue eliminado por la siguiente razón: ' +mot,
                    'icon': 'success'})
        return redirect('menu')

def proveedor(request, id):  # Mensajeria
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

# Modificar informacion

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
    producto.stockProducto = sto
    producto.descripcion = des
    if request.FILES.get('img') != None:
        producto.imagen = request.FILES['img']
    producto.save()
    messages.success(request,{
                    'title': 'Actualizado',
                    'text': 'Producto actualizado exitosamente!',
                    'icon': 'success'})
    return redirect('producto')


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
    messages.success(request,{
                    'title': 'Enviado',
                    'text': 'La solicitud fue respondida',
                    'icon': 'success'})
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
    messages.success(request,{
                    'title': 'Inventario actualizado',
                    'text': 'Se actualizo el inventario exitosamente!',
                    'icon': 'success'})
    return redirect('home')

def asignarUbicacion(request):
    idisbn = request.POST['id']
    est = request.POST['estante']
    comp = request.POST['compartimiento']

    inventario_prod = Inventario_producto.objects.get(id=idisbn)
    inventario_prod.estante = est
    inventario_prod.compartimiento = comp
    inventario_prod.save()
    messages.success(request,{
                    'title': 'Asignado',
                    'text': 'Se asigno correctamente la ubicación del producto.',
                    'icon': 'success'})
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
                messages.error(request,{
                    'title': 'Usuario inactivo',
                    'text': '',
                    'icon': 'success'})
        else:
            messages.error(request,{
                    'title': 'Error',
                    'text': 'Usuario y/o contraseña incorrecta.',
                    'icon': 'error'})
        return redirect('login')
    else:
        return render(request, 'login.html')

# LOGOUT

def logout_view(request):
    logout(request)
    return redirect('login')
