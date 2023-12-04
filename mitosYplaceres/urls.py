"""
URL configuration for mitosYplaceres project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from pathlib import Path
#from xml.etree.ElementInclude import include
from django.contrib import admin
from django.urls import path, include
from tiendaApp import views as vista
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', vista.inicioFront, name='inicio'),
    path('productos/', vista.inicio, name='inicioProductos'),
    #path('<str:id_categoria>/<str:categoria>/', vista.categoria, name='categoria'),
    path('<str:id_subcategoria>/<str:subcategoria>/<str:id_categoria>/<str:categoria>/', vista.productos, name='productos'),
    path('<str:id_subcategoria>/<str:subcategoria>/<str:id_categoria>/<str:categoria>/<str:producto_id>/editar/', vista.detalle_producto, name='detalle_producto'),
    path('<str:id_subcategoria>/<str:subcategoria>/<str:id_categoria>/<str:categoria>/<str:producto_id>/confirmar/', vista.eliminar_producto, name='productoDel'),
    path('perfiles/', vista.mostrar_perfiles, name="mostrar_perfiles"), 
    path('perfiles/mostrar_trabajadores/<int:perfil_id>/', vista.mostrar_trabajadores, name='mostrar_trabajadores'),

    path('detalle_trabajador/<int:trabajador_id>/<int:perfil_id>/', vista.editar_trabajador, name='editar_trabajador'),
    path('detalle_trabajador/elim_trabajador/<int:trabajador_id>/', vista.elim_trabajador, name='elim_trabajador'),
    path('buscar_trabajadores/', vista.buscar_trabajadores, name='buscar_trabajadores'),
    path('inicio/contacto', vista.enviar_mensaje, name='contacto' ),
    path('inicio/',vista.inicioUser, name= "inicioUsuario"),
    path('inicio/user/userAdd/', vista.crear_ususario, name='userAdd'),
    path('listaUsuarios/', vista.todos_usuarios, name="listaUsuarios"),
    path('listaUsuarios/usuarioEdit/<int:usuario_id>', vista.carga_editar_usuarios, name='editarUsuario'),
    path('usuarioEdit/usuarioEditado/<int:usuario_id>', vista.editar_usuario, name='usuarioEditado'),
    path('listaUsuarios/usuarioDelete/<int:usuario_id>', vista.eliminar_usuario, name='usuarioDelete'),
    
    path('accounts/', include('django.contrib.auth.urls')),
    path('inicioSesion/', vista.login_view, name='login'),
    path('cerrarSesion/', vista.logout_view, name='logout'),
    
    path('administracion/',vista.menu_admin, name='menu_admin'),
    path('administracion/mostrar_trabajadores/agregar_trabajador/', vista.agregar_trabajador, name='agregar_trabajador'),
    path('administracion/ingresar_producto', vista.compra_proveedor, name='compra_proveedor'),
    path('administracion/lista_clientes', vista.lista_clientes, name='lista_clientes'),
    path('administracion/lista_productos', vista.categorias_productos, name='categorias_productos'),
    path('administracion/ingresar_producto/registrar_producto/', vista.registro_producto, name='registro_producto'),
    path('administracion/lista_productos/<int:producto_id>/', vista.detalle_producto, name='detalle_producto'),
    path('administracion/mensajes_clientes', vista.lista_correos, name='lista_correos'),
    
    path('categorias/', vista.get_categorias, name='categorias'),
    path('subcategorias/<int:categoria_id>', vista.get_subcategorias, name='subcategorias'),
    path('producto/<int:categoria_id>/<int:subcategoria_id>', vista.get_productos, name='producto'),
    path('contacto/', vista.get_contacto, name='contacto'),
  
    path('buscador', vista.busqueda, name='buscador'),
    path('listaTipo', vista.listaTipo, name="listaTipo"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)