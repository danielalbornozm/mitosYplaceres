from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.views.generic.list import ListView
from django.views.generic import DetailView
from .models import Order, OrderLine
from tiendaApp.Carrito import Carrito


# Create your views here.
def process_order(request):
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

    cart.limpiar()

    messages.success(request, "El pedido se ha creado correctamente!")
    return redirect("tienda")


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

