from django.shortcuts import render
from tiendaApp.models import Producto
from django.http import JsonResponse
from tiendaApi.serializers import ProductoSerializar
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='inicio')
@api_view(['GET', 'POST'])
def producto_listado(request):
    if request.method == 'GET':
        productos = Producto.objects.all()
        serializer = ProductoSerializar(productos, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = ProductoSerializar(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@login_required(login_url='inicio')
@api_view(['GET', 'PUT', 'DELETE'])
def producto_detalle(request, pk):
    try:
        producto = Producto.objects.get(id=pk)
    except Producto.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = ProductoSerializar(producto)
        return Response(serializer.data)

    if request.method == 'PUT':
        serializer = ProductoSerializar(producto, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        producto.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Api RestFul

@login_required(login_url='inicio')
def productosApi(request):
    productos = Producto.objects.all()
    data = {
        'producto': list(
            productos.values('nombre', 'marca', 'precio', 'cantidad',
                             'categoria', 'subcategoria', 'descripcion')
        )
    }
    return JsonResponse(data)