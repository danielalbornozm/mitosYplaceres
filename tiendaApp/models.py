import datetime
from django import forms
from django.db import models
from django.utils import timezone
from tiendaApp.choices import primerJuguete
import os

# Create your models here.

# Clase categorías
class Categoria(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombre de la categoría")
    creado = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return "{}".format(self.nombre)
    
    class Meta:
        db_table = 'categoria'
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        
# Clase subcategorías
class Subcategoria(models.Model):
    categoria = models.ForeignKey(Categoria, null=False, on_delete=models.PROTECT)
    nombre = models.CharField(max_length=100, verbose_name="Nombre de la subcategoría")
    creado = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return "{}".format(self.nombre)
    
    class Meta:
        db_table = 'subcategoria'
        verbose_name = 'Subcategoria'
        verbose_name_plural = 'Subcategorias'
        
# Clase producto
class Producto(models.Model):
    nombre = models.CharField(max_length=200, verbose_name="Nombre del producto")
    marca = models.CharField(max_length=100, verbose_name="Marca del producto")
    precio = models.IntegerField(verbose_name="Precio del producto")
    cantidad = models.IntegerField(verbose_name="Stock del producto")
    categoria = models.ForeignKey(Categoria, null=False, on_delete=models.PROTECT)
    subcategoria = models.ForeignKey(Subcategoria, null=False, on_delete=models.PROTECT)
    primerJuguete = models.CharField(max_length=2, choices=primerJuguete, default='No')
    descripcion = models.CharField(max_length=1000, verbose_name="Descripción del producto")
    creado = models.DateTimeField(auto_now=True)
    
    def generarNombre(instance, filename):
        extension = os.path.splitext(filename)[1][1:]
        ruta = 'productos'
        fecha = timezone.now().strftime("%d%m%Y_%H%M%S")
        nombre = "{}.{}".format(fecha, extension)
        return os.path.join(ruta, nombre)
    
    foto = models.ImageField(upload_to=generarNombre,null=True,default='productos/producto.png')
    
    def __str__(self):
        return "{}".format(self.nombre)
    
    class Meta:
        db_table = 'producto'
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
    
    
    
    
        




