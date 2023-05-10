from django.urls import path
from rest.views import  vista_Producto,datos_producto,vista_Eliminar,datos_Eliminar,vista_Mensajeria,datos_Mensajeria
from rest.viewslogin import login
urlpatterns = [
    path('listaproductos',vista_Producto,name="listaproductos"),
    path('datosproductos/<id>',datos_producto,name="datosproductos"),

    path('listaeliminados',vista_Eliminar,name="listaeliminados"),
    path('datoseliminados/<id>',datos_Eliminar,name="datoseliminados"),

    path('listamen',vista_Mensajeria,name="listamen"),
    path('datosmen/<id>',datos_Mensajeria,name="datosmen"),
    
    path('logi',login,name="logi"),

]