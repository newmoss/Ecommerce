from django.contrib import admin
from .models import Producto,Motivo,Mensajeria,Tienda,Inventario,Inventario_producto

# Register your models here.
admin.site.register(Producto)
admin.site.register(Motivo)
admin.site.register(Mensajeria)
admin.site.register(Tienda)
admin.site.register(Inventario_producto)
admin.site.register(Inventario)
