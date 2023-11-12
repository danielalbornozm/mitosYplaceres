import datetime
from django import forms
from django.db import models
from django.utils import timezone
from tiendaApp.choices import primerJuguete

# Create your models here.

# Clase categorías
class Categoria(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombre de la categoría")
    creado = models.DateTimeField(default=timezone.now)
    
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
    creado = models.DateTimeField(default=timezone.now)
    
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
    primerJuguete = models.CharField(max_length=1, choices=primerJuguete, default='n')
    descripcion = models.CharField(max_length=100, verbose_name="Descripción del producto")
    creado = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return "{}".format(self.nombre)
    
    class Meta:
        db_table = 'producto'
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        




