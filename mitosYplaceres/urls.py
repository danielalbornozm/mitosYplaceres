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
from xml.etree.ElementInclude import include
from django.contrib import admin
from django.urls import path, include
from tiendaApp import views as vista
from django.conf import settings
from django.conf.urls.static import static
from tiendaApp.views import  mostrar_trabajadores, agregar_trabajador,editar_trabajador,elim_trabajador,mostrar_perfiles, enviar_mensaje

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', vista.inicio, name='inicio'),
    path('<str:id_categoria>/<str:categoria>/', vista.categoria, name='categoria'),
    path('<str:id_subcategoria>/<str:subcategoria>/<str:id_categoria>/<str:categoria>/', vista.productos, name='productos'),
    path('<str:id_subcategoria>/<str:subcategoria>/<str:id_categoria>/<str:categoria>/<str:producto_id>/mantenedor/', vista.mantenedor_productos, name='productoAdd'),
    path('<str:id_subcategoria>/<str:subcategoria>/<str:id_categoria>/<str:categoria>/<str:producto_id>/confirmar/', vista.eliminar_producto, name='productoDel'),
    path('perfiles/', mostrar_perfiles, name="mostrar_perfiles"),  # Corregido aquí
    path('perfiles/mostrar_trabajadores/<int:perfil_id>/', vista.mostrar_trabajadores, name='mostrar_trabajadores'),
    path('mostrar_trabajadores/agregar_trabajador/<int:perfil_id>/', agregar_trabajador, name='agregar_trabajador'),
    path('detalle_trabajador/<int:trabajador_id>/<int:perfil_id>/', editar_trabajador, name='editar_trabajador'),
    path('detalle_trabajador/elim_trabajador/<int:trabajador_id>/', elim_trabajador, name='elim_trabajador'),
    path('contacto', enviar_mensaje, name='contacto' ),
    path('accounts/',include('django.contrib.auth.urls')),
    path('inicio/',vista.inicioUser, name= "inicioUsuario"),
    path('inicio/user/userAdd/', vista.crear_ususario, name='userAdd'),
    path('listaUsuarios/', vista.todos_usuarios, name="listaUsuarios"),
    path('listaUsuarios/usuarioEdit/<int:usuario_id>', vista.carga_editar_usuarios, name='editarUsuario'),
    path('usuarioEdit/usuarioEditado/<int:usuario_id>', vista.editar_usuario, name='usuarioEditado'),
    path('listaUsuarios/usuarioDelete/<int:usuario_id>', vista.eliminar_usuario, name='usuarioDelete'),

    path('buscador', vista.busqueda, name='buscador'),
    path('listaTipo', vista.listaTipo, name="listaTipo"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)