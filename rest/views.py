from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt

from .serializers import ProductoSerializador,MensajeriaSerializador,EliminarSerializador
from core.models import Producto,Mensajeria,Motivo
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAdminUser, IsAuthenticated

@csrf_exempt
@api_view(['GET','POST'])
#@permission_classes((IsAuthenticated,))
def vista_Producto(request):
    if request.method == 'GET':
        m = Producto.objects.all()
        serializer = ProductoSerializador(m, many = True)
        return Response(serializer.data)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = ProductoSerializador(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)


@api_view(['GET','PUT','DELETE'])
#@permission_classes((IsAuthenticated,))
def datos_producto(request, id):
    try:
        m = Producto.objects.get(idMed = id)
    except Producto.DoesNotExist:
        return Response(status= status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = ProductoSerializador(m)
        return Response(serializer.data)
    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = ProductoSerializador(m, data = data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        m.delete()
        return Response(status= status.HTTP_204_NO_CONTENT)


#--------------------------MEDICAMENTO------------------------------------------------------------------

#----------------------------PRESCRIPCION-----------------------------------------------------------------------------------------

@api_view(['GET','POST'])
#@permission_classes((IsAuthenticated,))
def vista_Eliminar(request):
    if request.method == 'GET':
        m = Motivo.objects.all()
        serializer = EliminarSerializador(m, many = True)
        return Response(serializer.data)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = EliminarSerializador(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)


@api_view(['GET','PUT','DELETE'])
#@permission_classes((IsAuthenticated,))
def datos_Eliminar(request, id):
    try:
        m = Motivo.objects.get(idCad = id)
    except Motivo.DoesNotExist:
        return Response(status= status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = EliminarSerializador(m)
        return Response(serializer.data)
    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = EliminarSerializador(m, data = data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        m.delete()
        return Response(status= status.HTTP_204_NO_CONTENT)


#--------------------------------------------------------------------------------------------------------------------------



@api_view(['GET','POST'])
#@permission_classes((IsAuthenticated,))
def vista_Mensajeria(request):
    if request.method == 'GET':
        m = Mensajeria.objects.all()
        serializer = MensajeriaSerializador(m, many = True)
        return Response(serializer.data)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = MensajeriaSerializador(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)


@api_view(['GET','PUT','DELETE'])
#@permission_classes((IsAuthenticated,))
def datos_Mensajeria(request, id):
    try:
        m = Mensajeria.objects.get(idMen = id)
    except Mensajeria.DoesNotExist:
        return Response(status= status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = MensajeriaSerializador(m)
        return Response(serializer.data)
    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = MensajeriaSerializador(m, data = data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        m.delete()
        return Response(status= status.HTTP_204_NO_CONTENT)


#--------------------------------------------------------------------------------------------
