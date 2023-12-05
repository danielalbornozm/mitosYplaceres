from gettext import translation
from itertools import product
from typing_extensions import Self
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.test import TransactionTestCase
from django.db import transaction
from django.utils.html import strip_tags
from django.views.generic.list import ListView
from django.views.generic import DetailView

from tiendaApp.admin import ProductoAdmin
from tiendaApp.forms import ProductoForm
from .models import Order, OrderLine, Producto
from tiendaApp.Carrito import Carrito


# Create your views here.
def process_order(request):

    validarCarrito(request)

    order = Order.objects.create(user=request.user, completed=True)
    cart = Carrito(request)
    order_lines = list()

    for key, value in cart.carrito.items():
        
        order_lines.append(
            OrderLine(
                producto_id=key,
                cantidad=value["cantidad"],
                user=request.user,
                order=order
            )
        )        

    OrderLine.objects.bulk_create(order_lines)

    rebajarCarrito(request)

    cart.limpiar()

    messages.success(request, "El pedido se ha creado correctamente!")
    return redirect('tienda')

def validarCarrito(request): 

    cart = Carrito(request)

    for key, value in cart.carrito.items(): 
        if (value['cantidad'] <= get_object_or_404(Producto, pk=key).cantidad):
            messages.success(request, "Correcto!")
            print("ok")

        else:
            messages.success(request, "Incorrecto!")
            id = str(get_object_or_404(Producto, pk=key).pk)
            del cart.carrito[id]
            Carrito.guardar_carrito(cart)
            print("error")
            messages.success(request, "No hay suficiente stock para {}".format(str(get_object_or_404(Producto, pk=key).nombre)))

            return redirect('tienda')    
        
    return redirect('tienda')

def rebajarCarrito(request):

    cart = Carrito(request)

    for key, value in cart.carrito.items():
        producto = get_object_or_404(Producto, id=key)
        cantidad = value['cantidad']
        producto.reducir_cantidad(cantidad)
    
    return redirect('tienda')


class OrderList(ListView):
    model = Order
    ordering = ["-id"]
    template_name = "orders/listado.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)


class OrderDetail(DetailView):
    model = Order
    template_name = "orders/detalle.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)
    


