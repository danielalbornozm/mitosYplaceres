from django.shortcuts import render, redirect, get_object_or_404
from tiendaApp.models import Categoria, Subcategoria, Producto
from tiendaApp.forms import ProductoForm

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

def categoria(request, id_categoria, categoria):
    categorias = Categoria.objects.all()
    subcategorias = Subcategoria.objects.filter(categoria__nombre=categoria)
    productos = Producto.objects.all()
    data = {
        'id_categoria': id_categoria,
        'categoria': categoria,
        'categorias': categorias,
        'subcategorias': subcategorias,
        'productos': productos
    }
    return render(request, 'producto/categoria.html', data)

def productos(request, id_categoria, categoria, id_subcategoria, subcategoria):
    categorias = Categoria.objects.all()
    subcategorias = Subcategoria.objects.all()

    # Obtener el valor de búsqueda desde la consulta GET
    q = request.GET.get('q')

    # Filtrar productos según la búsqueda
    productos = Producto.objects.filter(subcategoria__id=id_subcategoria, categoria__id=id_categoria)
    if q:
        productos = productos.filter(nombre__icontains=q)

    data = {
        'id_subcategoria': id_subcategoria,
        'id_categoria': id_categoria,
        'categoria': categoria,
        'subcategoria': subcategoria,
        'categorias': categorias,
        'subcategorias': subcategorias,
        'productos': productos
    }
    return render(request, 'producto/productos.html', data)

def mantenedor_productos(request, id_categoria, categoria, id_subcategoria, subcategoria, producto_id):
    
    data = {
        'id_subcategoria': id_subcategoria,
        'id_categoria': id_categoria,
        'categoria': categoria,
        'subcategoria': subcategoria,
        'producto_id': producto_id
    }
    
    # Revisamos si producto_id tiene valor
    if producto_id == "0":
        producto = None
        form = ProductoForm()
    else:
        producto = get_object_or_404(Producto, id=producto_id)

    # Valores por defecto para los campos del formulario
    valores_iniciales = {
        'categoria': id_categoria,  # Ajusta el nombre según tu modelo
        'subcategoria': id_subcategoria,  # Ajusta el nombre según tu modelo
        # Otros campos si los tienes
    }

    # Métodos según el botón presionado    
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        print("Estamos")

        if 'guardar' in request.POST:
            if form.is_valid():
                form.save()
                print("Guardando")
                return redirect('productos', id_categoria, categoria, id_subcategoria, subcategoria)
            else:
                print(form.errors)
        elif 'editar' in request.POST:
            if form.is_valid():
                if 'foto' in request.FILES:
                    producto.foto = request.FILES['foto']
                form.save()
                print("Editando")
                return redirect('productos', id_categoria, categoria, id_subcategoria, subcategoria)
            else:
                print(form.errors)
    else:
        form = ProductoForm(initial=valores_iniciales, instance=producto)
        
    return render(request, 'producto/productoAdd.html', {'form': form, **data})

def eliminar_producto(request, id_categoria, categoria, id_subcategoria, subcategoria, producto_id):
    
    data = {
        'id_subcategoria': id_subcategoria,
        'id_categoria': id_categoria,
        'categoria': categoria,
        'subcategoria': subcategoria,
        'producto_id': producto_id
    }
    
    producto = get_object_or_404(Producto, id=producto_id)
    
    if request.method == 'POST':
        producto.delete()
        print("Eliminando")
        return redirect('productos', id_categoria, categoria, id_subcategoria, subcategoria)
    else:
        print("Problema")

    return render(request, 'producto/productoDel.html', {'producto':producto, **data})



