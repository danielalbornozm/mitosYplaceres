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
from django.contrib import admin
from django.urls import path
from tiendaApp import views as vista
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', vista.inicio, name='inicio'),
    path('<str:id_categoria>/<str:categoria>/', vista.categoria, name='categoria'),
    path('<str:id_subcategoria>/<str:subcategoria>/<str:id_categoria>/<str:categoria>/', vista.productos, name='productos'),
    path('<str:id_subcategoria>/<str:subcategoria>/<str:id_categoria>/<str:categoria>/<str:producto_id>/mantenedor/', vista.mantenedor_productos, name='productoAdd'),
    path('<str:id_subcategoria>/<str:subcategoria>/<str:id_categoria>/<str:categoria>/<str:producto_id>/confirmar/', vista.eliminar_producto, name='productoDel'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)