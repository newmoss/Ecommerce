from django.db import models
from django.db.models.base import Model
from django.db.models.fields import CharField, IntegerField

# Create your models here.

class Producto(models.Model):
    idProducto = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    precio = IntegerField()
    stock = IntegerField()
    descripcion = models.CharField(max_length=500)
    imagen = models.ImageField(upload_to="Imagenes",null=True)

    def __str__(self):
        return self.nombre

class Motivo(models.Model):
    idMotivo = models.AutoField(primary_key=True)
    codigo = models.IntegerField()
    productoEliminado = models.CharField(max_length=50)
    motivo = models.CharField(max_length=100)
    def __str__(self):
        return self.productoEliminado


class Mensajeria(models.Model):
    idMen = models.AutoField(primary_key=True)
    nombreApe = models.CharField(max_length=100)
    email = models.CharField(max_length=50)
    telefono = models.CharField(max_length=20)
    medicamento = models.CharField(max_length=100)
    cantidad = models.CharField(max_length=20)

    def __str__(self):
        return self.nombreApe
