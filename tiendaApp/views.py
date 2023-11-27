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
    else:
        form = ProductoForm(initial=valores_iniciales, instance=producto)
        
    return render(request, 'producto/productoAdd.html', {'form': form, **data})

def detalle_producto(request, id_categoria, categoria, id_subcategoria, subcategoria, producto_id):
    
    producto = get_object_or_404(Producto, id=producto_id)
    
    data = {
        'id_subcategoria': id_subcategoria,
        'id_categoria': id_categoria,
        'categoria': categoria,
        'subcategoria': subcategoria,
        'producto_id': producto_id,
        'foto': producto.foto,
    }
    
    producto = get_object_or_404(Producto, id=producto_id)

    # Métodos según el botón presionado    
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        print("Estamos")

        if 'editar' in request.POST:
            if form.is_valid():
                if 'foto' in request.FILES:
                    producto.foto = request.FILES['foto']
                form.save()
                print("Editando")
                return redirect('productos', id_categoria, categoria, id_subcategoria, subcategoria)
            else:
                print(form.errors)
    else:
        form = ProductoForm(instance=producto)
        
    return render(request, 'producto/detalle_producto.html', {'form': form, **data})

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

################################################################################################

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import PerfilTrabajador, Trabajador, MensajeContacto
from .forms import TrabajadorForm, TrabajadorEditForm, ContactoForm
from django.db.models import Q
from django.core.mail import send_mail
from django.http import JsonResponse

# Create your views here.
def mostrar_perfiles(request):
    perfiles = PerfilTrabajador.objects.all()
    
    data = {'perfiles': perfiles}
    
    return render(request,'Trabajadores/perfiles.html', data)

def mostrar_trabajadores(request, perfil_id):
    
    print(f"Vista mostrar_trabajadores alcanzada con perfil_id: {perfil_id}")
    
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

def agregar_trabajador(request, perfil_id):
    perfil = PerfilTrabajador.objects.get(pk=perfil_id)

    if request.method == 'POST':
        form = TrabajadorForm(request.POST, request.FILES)
        if form.is_valid():
            contraseña = form.cleaned_data.get('contraseña')
            confirmar_contraseña = request.POST.get('confirmar_contraseña')

            if contraseña == confirmar_contraseña:
                trabajador = form.save(commit=False)
                trabajador.perfil = perfil
                trabajador.save()
                messages.success(request, 'Trabajador registrado con éxito.')
                return redirect('mostrar_trabajadores', perfil_id=perfil_id)
            else:
                messages.error(request, 'Las contraseñas no coinciden.')
        else:
            print(form.errors)
    else:
        form = TrabajadorForm()

    return render(request, 'Trabajadores/agregar_trabajador.html', {'perfil': perfil, 'form': form})



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


            return redirect('contacto')
    else:
        form = ContactoForm()

    return render(request, 'producto/contacto.html', {'form': form})

def buscar_trabajadores(request):
    # Obtener el valor de búsqueda de la solicitud GET
    query = request.GET.get('q', '')

    # Filtrar los trabajadores según el valor de búsqueda
    trabajadores = Trabajador.objects.filter(nombre__icontains=query)

    # Renderizar los resultados en un fragmento de HTML
    return render(request, 'trabajadores/fragmento_resultados_busqueda.html', {'trabajadores': trabajadores})

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
    return render(request, 'userTemplates/listaUsuarios.html', data)

def listaTipo(request):    
    q = request.GET.get('q')
    datos = Usuario.objects.filter(tipo=q)
    tipos = Tipo.objects.all()

    data = {
        'usuarios': datos, 
        'tipos': tipos,
    }
    return render(request, 'userTemplates/listaUsuarios.html', data)



