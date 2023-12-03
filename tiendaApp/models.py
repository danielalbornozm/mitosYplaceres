import datetime
from django import forms
from django.db import models
from django.utils import timezone
from tiendaApp.choices import primerJuguete, sexos
import os
from django.core.validators import MinLengthValidator

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
        
###########################################################################################

# Clase Perfil trabajador
class PerfilTrabajador(models.Model):
    cargo = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=200)
    foto = models.ImageField(upload_to='media/fotos_perfiles/', blank=True, null=True)

    def __str__(self):
        return self.cargo
    
    class Meta:
        db_table = 'perfil trabajador'
        verbose_name = 'perfil trabajador'
        verbose_name_plural = 'perfil trabajadores'
    
# Clase trabajador
class Trabajador(models.Model):
    perfil = models.ForeignKey(PerfilTrabajador, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    paterno = models.CharField(max_length=100)
    materno = models.CharField(max_length=100)
    sexo = models.CharField(max_length=1, choices=[('M', 'Masculino'), ('F', 'Femenino')])
    rut = models.CharField(max_length=12)
    fecha_nacimiento = models.DateField()
    telefono = models.CharField(max_length=15)
    correo = models.EmailField()
    contraseña = models.CharField(max_length=255, validators=[MinLengthValidator(6)])  
    foto = models.ImageField(upload_to='fotos_trabajadores', blank=True, null=True)

    def __str__(self):
        return f"{self.nombre} {self.paterno} {self.materno}"
    
    class Meta:
        db_table = 'trabajador'
        verbose_name = 'trabajador'
        verbose_name_plural = 'trabajadores'
    
# Clase mensaje contacto
class MensajeContacto(models.Model):
    nombre = models.CharField(max_length=255)
    apellido = models.CharField(max_length=255)
    correo = models.EmailField()
    mensaje = models.TextField()

    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.correo}"   
    

##################################################################################################

# Clase tipo
class Tipo(models.Model):
    nombre = models.CharField(max_length=100, verbose_name = 'Nombre del Tipo')
    descripcion = models.CharField(max_length=200, verbose_name = 'Descripcion del Tipo')
    creado = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "{}".format(self.nombre)
    
    class Meta:
        db_table = 'tipo'
        verbose_name = 'Tipo'
        verbose_name_plural = 'Tipos'

# Clase usuario
class Usuario(models.Model):
    run = models.CharField(max_length=10, verbose_name='RUN')
    nombre = models.CharField(max_length=50, verbose_name='Nombre')
    paterno = models.CharField(max_length=50, verbose_name='Apellido Paterno')
    materno = models.CharField(max_length=50, verbose_name='Apellido Materno', blank=True)
    sexo = models.CharField(max_length=1, choices=sexos, default='m')
    direccion = models.CharField(max_length=100, verbose_name='Direccion')
    correo = models.CharField(max_length=50, verbose_name='E-Mail')
    fechaNac = models.DateField(blank=True, null=True, verbose_name='Fecha de Nacimiento')
    tipo = models.ForeignKey(Tipo,null=False,on_delete=models.RESTRICT)
    creado = models.DateTimeField(default=timezone.now, editable=False)

    def generarNombre(instance,filename):
        extension = os.path.splitext(filename)[1][1:]
        ruta = 'usuarios'
        fecha = timezone.now().strftime("%d%m%Y_%H%M%S")
        nombre = "{}.{}".format(fecha,extension)
        return os.path.join(ruta,nombre)
    foto = models.ImageField(upload_to=generarNombre, null=True, default='usuarios/usuario.png')

    def __str__(self):
        return "{} {} {}".format(self.nombre,self.paterno,self.materno)
    
    class Meta:
        db_table = 'usuario'
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        ordering = ['nombre','paterno','materno'] 
    
        




