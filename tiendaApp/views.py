from django.shortcuts import render, redirect, get_list_or_404
from tiendaApp.models import Categoria, Subcategoria, Producto
#from tiendaApp.forms import CategoriaForm

# Create your views here.
def inicio(request):
    categorias = Categoria.objects.all()
    subcategoria = Subcategoria.objects.all()
    productos = Producto.objects.all()
    data = {
        'categorias': categorias,
        'subcategorias': subcategoria,
        'productos': productos
    }
    return render(request, 'producto/inicio.html', data)
