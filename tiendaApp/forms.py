import datetime
from django import forms
from tiendaApp.choices import primerJuguete
from tiendaApp.models import Categoria, Subcategoria, Producto

class ProductoForm(forms.ModelForm):
    nombre = forms.CharField(widget=forms.TextInput(
        attrs={'class':'form-control', 'placeholder': 'Ingrese nombre del producto'}))
    marca = forms.CharField(widget=forms.TextInput(
        attrs={'class':'form-control', 'placeholder': 'Ingrese marca del producto'}))
    precio = forms.IntegerField(widget=forms.NumberInput(
        attrs={'class':'form-control', 'placeholder': 'Ingrese precio del producto'}))
    cantidad = forms.IntegerField(widget=forms.NumberInput(
        attrs={'class':'form-control', 'placeholder': 'Ingrese cantidad del del producto'}))
    primerJuguete = forms.CharField(widget=forms.Select(choices=primerJuguete,
        attrs={'class':'form-select'}))
    descripcion = forms.CharField(widget=forms.Textarea(
        attrs={'class':'form-control', 'rows': 5, 'placeholder': 'Ingrese descripción del producto'}))
    categoria = forms.ModelChoiceField(
        queryset = Categoria.objects.all(),
        empty_label = "Seleccione categoria",
        widget = forms.Select(attrs={'class':'form-select'}))
    subcategoria = forms.ModelChoiceField(
        queryset = Subcategoria.objects.all(),
        empty_label = "Seleccione subcategoría",
        widget = forms.Select(attrs={'class':'form-select'}))
    
    # Indicamos los campos del formulario cuando llamamos a la clase
    class Meta: 
        model = Producto
        fields = '__all__'
    
    """
    # Validación
    def clean_fechaNac(self):
        fechaNac = self.cleaned_data.get('fechaNac')
        fecha_minima = datetime.date(1920, 1, 1)
        fecha_maxima = datetime.date(2005, 1, 1)
        
        if fechaNac < fecha_minima or fechaNac > fecha_maxima:
            raise forms.ValidationError("Debe ingresar fecha de nacimiento válida")
        
        return fechaNac
    """
    
###################################################################################

from .models import Trabajador, PerfilTrabajador, MensajeContacto

class TrabajadorForm(forms.ModelForm):
    # Campo adicional para confirmar contraseña
    confirmar_contraseña = forms.CharField(widget=forms.PasswordInput(), label='Confirmar Contraseña')

    class Meta:
        model = Trabajador
        fields = ['nombre', 'paterno', 'materno', 'sexo', 'rut', 'fecha_nacimiento', 'telefono', 'correo', 'contraseña', 'confirmar_contraseña', 'foto']
        widgets = {
            'fecha_nacimiento': forms.SelectDateWidget(years=range(1900, 2024)),  
            'contraseña': forms.PasswordInput(),
        }

    def clean(self):
        cleaned_data = super().clean()
        contraseña = cleaned_data.get('contraseña')
        confirmar_contraseña = cleaned_data.get('confirmar_contraseña')

        # Verifica si las contraseñas coinciden
        if contraseña != confirmar_contraseña:
            raise forms.ValidationError('Las contraseñas no coinciden.')

        return cleaned_data

class TrabajadorEditForm(forms.ModelForm):
    class Meta:
        model = Trabajador
        fields = ['nombre', 'paterno', 'materno', 'sexo', 'rut', 'fecha_nacimiento', 'telefono', 'correo', 'contraseña', 'foto']
        widgets = {
            'fecha_nacimiento': forms.SelectDateWidget(years=range(1900, 2024)),  
    
        }  
         
             

    # Agregar campo de selección para el perfil
    perfil = forms.ModelChoiceField(queryset=PerfilTrabajador.objects.all(), required=False)



class ContactoForm(forms.ModelForm):
    class Meta:
        model = MensajeContacto
        fields = ['nombre', 'apellido', 'correo', 'mensaje']
        widgets = {
            'nombre': forms.TextInput(attrs={'style': 'width: 100%; max-width: 560px;'}),
            'apellido': forms.TextInput(attrs={'style': 'width: 100%; max-width: 560px;'}),
            'correo': forms.TextInput(attrs={'style': 'width: 100%; max-width: 560px;'}),
            'mensaje': forms.Textarea(attrs={'style': 'width: 100%; max-width: 560px;'}),
        }
        
        
###############################################################################################

from dataclasses import field
from tkinter.tix import Select
from django import forms
from tiendaApp.choices import sexos
from tiendaApp.models import Tipo, Usuario
import datetime


class UsuarioForms(forms.ModelForm):
    run = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'EJ: 16839387-3'}))
    run = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'EJ: 16839387-3'}))
    nombre = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Ingrese Nombre'}))
    paterno = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Ingrese Apellido Paterno'}))
    materno = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Ingrese Apellido Materno'}), required=False)
    sexo = forms.CharField(widget=forms.Select(choices=sexos, attrs={'class':'form-select'}))
    fechaNac = forms.DateField(widget=forms.DateInput(attrs={'class':'form-control','placeholder':'dia/mes/año', 'type': 'date'}))
    direccion = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Ingrese Direccion de Envio'}))
    correo = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Ingrese Correo (E-Mail)'}))


    tipo = forms.ModelChoiceField(
        queryset=Tipo.objects.all(),
        empty_label='Seleccione un Tipo de Cliente',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Usuario
        fields = '__all__'    
    
    def clean_fechaNac(self):
        fecha_nacimiento = self.cleaned_data.get('fechaNac') 

        fecha_minima = datetime.date(1920, 1, 1)
        fecha_maxima = datetime.date(2023,11,13)

        if fecha_nacimiento:
            if fecha_nacimiento < fecha_minima or fecha_nacimiento > fecha_maxima:
                raise forms.ValidationError("La fecha de nacimiento debe estar entre los años 1920 y 2005")
        return fecha_nacimiento
    
    def clean_nombre(self):
        nombre = self.cleaned_data.get("nombre")
        if nombre and not nombre.isalpha() and ' ' not in nombre:
            raise forms.ValidationError("El nombre debe contener solo letras y espacios")
        return nombre