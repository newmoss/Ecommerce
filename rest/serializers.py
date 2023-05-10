from core.models import Mensajeria,Producto,Motivo
from rest_framework import serializers

class ProductoSerializador(serializers.ModelSerializer):

    class Meta:
        model = Producto
        fields = ['idProducto','nombre','precio','stock','descripcion','imagen']


class MensajeriaSerializador(serializers.ModelSerializer):

    class Meta:
        model = Mensajeria
        fields = '__all__'

class EliminarSerializador(serializers.ModelSerializer):

    class Meta:
        model = Motivo
        fields = '__all__'

