from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from rest_framework.authtoken.models import Token

@api_view(['POST'])
def login(request):
    data = JSONParser().parse(request)
    u = data['username']
    c = data['password']

    try:
        user = User.objects.get(username = u)
    except User.DoesNotExist:
        return Response("El usuario no existe")
    pass_valido = check_password( c,user.password )

    if not pass_valido:
        return Response("Contraseña Incorrecta")

    #Permite crea el token u obtenerlo
    token, created = Token.objects.get_or_create(user = user)
    return Response(token.key)