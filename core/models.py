from django.db import models
from django.db.models.base import Model
from django.db.models.fields import CharField, IntegerField
from datetime import datetime

# Create your models here.
class Tienda(models.Model):
    idTienda = models.AutoField(primary_key=True)
    nombreTienda = models.CharField(max_length=50)
    direccion = models.CharField(max_length=50)
    imagenTienda = models.ImageField(upload_to="Tiendas",null=True)

    def __str__(self):
        return self.nombreTienda

class Producto(models.Model):
    idProducto = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    precio = IntegerField()
    descripcion = models.CharField(max_length=500)
    imagen = models.ImageField(upload_to="Productos",null=True)

    def __str__(self):
        return self.nombre
    
class Inventario(models.Model):
    idInventario = models.AutoField(primary_key=True)
    inventario = models.CharField(max_length=20)
    tienda= models.ForeignKey(Tienda, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.inventario


class Usuario(models.Model):
    idUsuario = models.AutoField(primary_key=True)
    nombres = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    inventarioId =  models.ForeignKey(Inventario, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.nombres

class Inventario_producto(models.Model):
    inventarioId =  models.ForeignKey(Inventario, on_delete=models.CASCADE, null=True)
    productoId =  models.ForeignKey(Producto, on_delete=models.CASCADE, null=True)
    stock = models.IntegerField()
    estante = models.CharField(max_length=50,null=True)
    compartimiento = models.CharField(max_length=50,null=True)


class Motivo(models.Model):
    idMotivo = models.AutoField(primary_key=True)
    codigo = models.IntegerField()
    productoEliminado = models.CharField(max_length=50)
    motivo = models.CharField(max_length=100)
    fecha = models.DateTimeField(default=datetime.now, editable=False)

    
    def __str__(self):
        return self.productoEliminado
    
class estadoSolicitud(models.Model):
    idEstado = models.AutoField(primary_key=True)
    estadoSol = models.CharField(max_length=50)
    
    def __str__(self):
        return self.estadoSol
    
class Solicitud(models.Model):
    idSolicitud = models.AutoField(primary_key=True)
    productoSolicitado = models.CharField(max_length=50)
    estadoSol= models.ForeignKey(estadoSolicitud, on_delete=models.CASCADE, null=True)
    fechaSolicitud = models.DateTimeField(default=datetime.now, editable=False)
    inventarioId = models.ForeignKey(Inventario, on_delete=models.CASCADE, null=True)
    respuesta = models.CharField(max_length=50)
    
    def __str__(self):
        return self.productoSolicitado

class Mensajeria(models.Model):
    idMen = models.AutoField(primary_key=True)
    nombreApe = models.CharField(max_length=100)
    email = models.CharField(max_length=50)
    telefono = models.CharField(max_length=20)
    medicamento = models.CharField(max_length=100)
    cantidad = models.CharField(max_length=20)
    
    def __str__(self):
        return self.nombreApe
    

