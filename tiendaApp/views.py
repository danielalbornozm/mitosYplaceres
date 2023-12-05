from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import permission_required
from tiendaApp.models import Categoria, Subcategoria, Producto, CompraProveedor
from tiendaApp.Carrito import Carrito
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

"""
def categoria(request, id_categoria, categoria):
    
    print(f"Vista mostrar_trabajadores alcanzada con perfil_id: {id_categoria}")
    
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
"""

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

def mantenedor_productos(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)

        if form.is_valid():
            producto = form.save(commit=False)

            producto.save()

            messages.success(request, 'Producto registrado con éxito.')
            return redirect('menu_admin')  
        else:
            print(form.errors)
    else:
        form = ProductoForm()

    print("Estamos aquí")  # Agrega mensajes de depuración
    return render(request, 'producto/productoAdd.html', {'form': form})


def detalle_producto(request, producto_id, id_categoria=None, id_subcategoria=None, subcategoria=None):
    
    producto = get_object_or_404(Producto, id=producto_id)
    
    data = {
        'id_subcategoria': id_subcategoria,
        'id_categoria': id_categoria,
        #'categoria': categoria,
        'subcategoria': subcategoria,
        'producto_id': producto_id,
        'foto': producto.foto,
    }
    
    producto = get_object_or_404(Producto, id=producto_id)

    # Métodos según el botón presionado    
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        print("Estamos")

        if 'guardar' in request.POST:
            print("aquí")
            if form.is_valid():
                if 'foto' in request.FILES:
                    producto.foto = request.FILES['foto']
                form.save()
                print("Editando")
                return redirect('categorias_productos')
            else:
                print(form.errors)
    else:
        form = ProductoForm(instance=producto)
        
    return render(request, 'producto/detalle_producto.html', {'form': form, **data})

def eliminar_producto(request, producto_id):
    
    data = {
        
        'producto_id': producto_id
    }
    
    producto = get_object_or_404(Producto, id=producto_id)
    
    if request.method == 'POST':
        producto.delete()
        print("Eliminando")
        return redirect('categorias_productos')
    else:
        print("Problema")

    return render(request, 'producto/productoDel.html', {'producto':producto, **data})

################################################################################################

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import PerfilTrabajador, Trabajador, MensajeContacto
from .forms import TrabajadorForm, TrabajadorEditForm, ContactoForm, CompraProveedorForm, DetalleCompraForm
from django.db.models import Q
from django.core.mail import send_mail
from django.http import JsonResponse
import os
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='inicio')
def menu_admin(request):
    return render(request, 'Trabajadores/Administrador.html')

@login_required(login_url='inicio')
def mostrar_perfiles(request):
    perfiles = PerfilTrabajador.objects.all()
    
    data = {'perfiles': perfiles}
    
    return render(request,'Trabajadores/perfiles.html', data)

@login_required(login_url='inicio')
def mostrar_trabajadores(request, perfil_id):
    
    
    perfil = PerfilTrabajador.objects.get(id=perfil_id)

    trabajadores = Trabajador.objects.filter(perfil=perfil)

    query = request.GET.get('q')
    if query:
        trabajadores = trabajadores.filter(
            Q(nombre__icontains=query) |
            Q(paterno__icontains=query) |
            Q(materno__icontains=query)
        )

    return render(request, 'Trabajadores/mostrar_trabajadores.html', {'perfil': perfil, 'trabajadores': trabajadores})

@login_required(login_url='inicio')
def agregar_trabajador(request):

    if request.method == 'POST':
        form = TrabajadorForm(request.POST, request.FILES)
        if form.is_valid():
            contraseña = form.cleaned_data.get('contraseña')
            confirmar_contraseña = request.POST.get('confirmar_contraseña')

            if contraseña == confirmar_contraseña:
                trabajador = form.save(commit=False)
            
                trabajador.save()
                messages.success(request, 'Trabajador registrado con éxito.')
                return redirect('menu_admin')
            else:
                messages.error(request, 'Las contraseñas no coinciden.')
        else:
            print(form.errors)
    else:
        form = TrabajadorForm()

    return render(request, 'Trabajadores/agregar_trabajador.html', {'form': form})

@login_required(login_url='inicio')
def editar_trabajador(request, trabajador_id, perfil_id):
    trabajador = get_object_or_404(Trabajador, id=trabajador_id)

    if request.method == 'POST':
        form = TrabajadorEditForm(request.POST, request.FILES, instance=trabajador)
        if form.is_valid():
            trabajador_form = form.save(commit=False)

            # Verifica si se proporcionó un perfil y asigna al trabajador
            nuevo_perfil_id = form.cleaned_data.get('perfil')
            if nuevo_perfil_id is not None:
                nuevo_perfil = get_object_or_404(PerfilTrabajador, id=nuevo_perfil_id.id)
                trabajador_form.perfil = nuevo_perfil


            # Guarda el trabajador con los cambios en el perfil
            trabajador_form.save()

            return redirect('mostrar_trabajadores', perfil_id=perfil_id)

    else:
        form = TrabajadorEditForm(instance=trabajador)

    return render(request, 'Trabajadores/detalle_trabajador.html', {'trabajador': trabajador, 'form_edicion': form})

@login_required(login_url='inicio')
def elim_trabajador(request, trabajador_id):
    trabajador = get_object_or_404(Trabajador, id=trabajador_id)

    perfil_id = trabajador.perfil.id  

    trabajador.delete()

    return redirect('mostrar_trabajadores', perfil_id=perfil_id)

def enviar_mensaje(request):
    if request.method == 'POST':
        form = ContactoForm(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            apellido = form.cleaned_data['apellido']
            correo = form.cleaned_data['correo']
            mensaje = form.cleaned_data['mensaje']

            # Crear un nuevo objeto MensajeContacto y guardar en la base de datos
            nuevo_mensaje = MensajeContacto(nombre=nombre, apellido=apellido, correo=correo, mensaje=mensaje)
            nuevo_mensaje.save()
            
            # Limpiar los campos del formulario
            form = ContactoForm()
            
            # Agregar un mensaje a través del contexto para indicar que el mensaje fue enviado
            return render(request, 'producto/contacto.html', {'mensaje_enviado': True, 'form': form})
        
    else:
        form = ContactoForm()

    return render(request, 'producto/contacto.html', {'form': form})

@login_required(login_url='inicio')
def buscar_trabajadores(request):
    # Obtener el valor de búsqueda de la solicitud GET
    query = request.GET.get('q', '')

    # Filtrar los trabajadores según el valor de búsqueda
    trabajadores = Trabajador.objects.filter(nombre__icontains=query)

    # Renderizar los resultados en un fragmento de HTML
    return render(request, 'trabajadores/fragmento_resultados_busqueda.html', {'trabajadores': trabajadores})

@login_required(login_url='inicio')
@permission_required('tiendaApp.menu_admin', login_url='menu_admin')
def compra_proveedor(request):
    cantidad_productos_range = range(1, 11)

    if request.method == 'POST':
        form = CompraProveedorForm(request.POST)
        detalle_form = DetalleCompraForm(request.POST)

        if form.is_valid() and detalle_form.is_valid():
            compra_principal = form.save()

            nombre_producto = detalle_form.cleaned_data['producto']


            producto = Producto.objects.get(nombre=nombre_producto)

            detalle = detalle_form.save(commit=False)
            detalle.compra = compra_principal
            detalle.save()

            producto.cantidad += detalle.cantidad
            producto.save()

            return redirect('menu_admin')
    else:
        form = CompraProveedorForm()
        detalle_form = DetalleCompraForm()

    return render(request, 'Trabajadores/compra_proveedor.html', {'form': form, 'detalle_form': detalle_form, 'cantidad_productos_range': cantidad_productos_range})

@login_required(login_url='inicio')
def lista_clientes(request):
    usuarios = Usuario.objects.all()
    tipos = Tipo.objects.all()

    query = request.GET.get('q')
    if query:
        usuarios = usuarios.filter(
            Q(nombre__icontains=query) |
            Q(paterno__icontains=query) |
            Q(materno__icontains=query) 
        )
    

    data = {
        'usuarios': usuarios, 
        'tipos': tipos,
    }
    return render(request, 'Trabajadores/lista_clientes.html', data)

@login_required(login_url='inicio')
def categorias_productos(request):
    categorias = Categoria.objects.all()
    subcategoria = Subcategoria.objects.all()
    productos = Producto.objects.all()

    query = request.GET.get('q')
    if query:
        productos = productos.filter(
            Q(nombre__icontains=query) |
            Q(marca__icontains=query) 

        )
    data = {
        'categorias': categorias,
        'subcategorias': subcategoria,
        'productos': productos
    }
    
    return render(request, 'Trabajadores/lista_productos.html', data)

@login_required(login_url='inicio')
def registro_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)

        if form.is_valid():
            producto = form.save(commit=False)
            producto.save()

            messages.success(request, 'Producto registrado con éxito.')
            return redirect('compra_proveedor') 
        else:
            print(form.errors)
    else:
        form = ProductoForm()

    
    return render(request, 'Trabajadores/registro_producto.html', {'form': form})

@login_required(login_url='inicio')
def lista_correos(request):
    mensajes = MensajeContacto.objects.all()
    print(mensajes)
    
    return render(request, 'Trabajadores/lista_correos.html', {'mensajes': mensajes})

@login_required(login_url='inicio')
def lista_facturas(request):
    compras = CompraProveedor.objects.all()
    return render(request, 'Trabajadores/lista_facturas.html', {'compras': compras})

############################################################################################################

from ast import arg
from imp import PKG_DIRECTORY
from urllib.request import Request
from xml.dom.minidom import Identified
from django.shortcuts import get_object_or_404, render, redirect
import pkg_resources
from tiendaApp import models as datos
from tiendaApp.forms import UsuarioForms
from tiendaApp.models import Tipo, Usuario

# Create your views here.

def inicioUser(request):
    tipos = Tipo.objects.all()

    data = {
        'tipos': tipos, 
    }
    return render(request, 'userTemplates/inicio.html', data)

def crear_ususario(request):
    if request.method == 'POST':
        form = UsuarioForms(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/listaUsuarios/')
    else:
        form = UsuarioForms()
    return render(request,'userTemplates/userAdd.html',{'form':form})

def todos_usuarios(request):
    usuarios = Usuario.objects.all()
    tipos = Tipo.objects.all()

    data = {
        'usuarios': usuarios, 
        'tipos': tipos,
    }
    return render(request, 'userTemplates/listaUsuarios.html', data)


def carga_editar_usuarios(request,usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)
    form = UsuarioForms(instance=usuario)
    return render(request, 'userTemplates/usuarioEdit.html',{'form':form, 'usuario':usuario})

def editar_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)

    if request.method == 'POST':
        form = UsuarioForms(request.POST, request.FILES, instance=usuario)
        if form.is_valid():
            if 'foto' in request.FILES:
                usuario.foto = request.FILES['foto']
            form.save()
            return redirect('/listaUsuarios/')
    else:
        form = UsuarioForms(instance=usuario)
    return render(request, 'userTemplates/listaUsuarios.html', {'form':form})

def eliminar_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)

    if request.method == 'POST':
        usuario.delete()
        return redirect('/listaUsuarios/')
    return render(request, 'userTemplates/usuarioDelete.html', {'usuario':usuario})

def busqueda(request):
    q = request.GET.get('q')
    datos = Usuario.objects.filter(nombre__icontains=q)
    tipos = Tipo.objects.all()

    data = {
        'usuarios': datos, 
        'tipos': tipos,
    }
    return render(request, 'Trabajadores/lista_clientes.html', data)

def listaTipo(request):    
    q = request.GET.get('q')
    datos = Usuario.objects.filter(tipo=q)
    tipos = Tipo.objects.all()

    data = {
        'usuarios': datos, 
        'tipos': tipos,
    }
    return render(request, 'userTemplates/listaUsuarios.html', data)

#########################################################################################################

# FRONT END

def inicioFront(request):
    categorias = Categoria.objects.all()
    subcategoria = Subcategoria.objects.all()
    productos = Producto.objects.all()
    data = {
        'categorias': categorias,
        'subcategorias': subcategoria,
        'productos': productos
    }
    return render(request, 'frontEnd/inicio.html', data)


#########################################################################################################

# INICIO DE SESION

from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # Obtener la URL a la que se debe redirigir
                next_url = request.GET.get('next', 'menu_admin')
                # Redirigir a la página deseada después del inicio de sesión
                return redirect(next_url)
            else:
                # El usuario no pudo ser autenticado, puedes manejar esto de alguna manera
                pass
    else:
        form = AuthenticationForm()

    return render(request, 'registration/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('inicio')


##########################################################################################################

# Funciones para Django Front End

from .models import Categoria, Subcategoria, Producto 

def get_categorias(_request):
    categoria = list(Categoria.objects.values())
    
    if (len(categoria) > 0):
        data = {'message':"Éxito", 'categoria':categoria}
    else:
        data = {'message':"Sin datos"}
        
    return JsonResponse(data)

def get_subcategorias(_request, categoria_id):
    subcategoria = list(Subcategoria.objects.filter(categoria = categoria_id).values())
    
    if (len(subcategoria) > 0):
        data = {'message':"Éxito", 'subcategoria':subcategoria}
    else:
        data = {'message':"Sin datos"}
        
    return JsonResponse(data)

def get_productos(_request, categoria_id, subcategoria_id):
    productos = list(Producto.objects.filter(categoria = categoria_id, subcategoria = subcategoria_id))
    
    if (len(productos) > 0):
        data = {'message':"Éxito", 'productos': [
            {
                'nombre': producto.nombre,
                'foto': producto.foto.url,
                'precio': producto.precio,
                'cantidad': producto.cantidad,   
            }
            for producto in productos
        ]}
    else:
        data = {'message':"Sin datos"}
        
    return JsonResponse(data)

"""
def get_contacto(_request):
    contacto = list(MensajeContacto.objects.values())
    
    if (len(contacto) > 0):
        data = {'message':"Éxito", 'contacto':contacto}
    else:
        data = {'message':"Sin datos"}
        
    return JsonResponse(data)
"""

###################################################################################################################

#Vistas Carrito

def tienda(request):
    productos = Producto.objects.all()
    return render(request, "ventas/tienda.html", {'productos':productos})

def agregar_producto(request, producto_id):
    carrito = Carrito(request)
    producto = Producto.objects.get(id=producto_id)
    carrito.agregar(producto)
    return redirect("tienda")

def eliminar_producto(request, producto_id):
    carrito = Carrito(request)
    producto = Producto.objects.get(id=producto_id)
    carrito.eliminar(producto)
    return redirect("tienda")

def restar_producto(request, producto_id):
    carrito = Carrito(request)
    producto = Producto.objects.get(id=producto_id)
    carrito.restar(producto)
    return redirect("tienda")

def limpiar_carrito(request):
    carrito = Carrito(request)
    carrito.limpiar()
    return redirect("tienda")

def buscar_producto(request):
    productos = Producto.objects.all()

    # Obtener el valor de búsqueda desde la consulta GET
    q = request.GET.get('q')

    # Filtrar productos según la búsqueda
    if q:
        productos = productos.filter(nombre__icontains=q)

    data = {
        'productos': productos
    }
    return render(request, 'ventas/tienda.html', data)

