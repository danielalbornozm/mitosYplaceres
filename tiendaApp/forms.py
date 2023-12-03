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

from django.core.exceptions import ValidationError
from django.forms import inlineformset_factory
from django.core.validators import validate_email
from datetime import date
import re
from .models import Trabajador, PerfilTrabajador, MensajeContacto, CompraProveedor,DetalleCompra

class TrabajadorForm(forms.ModelForm):
    confirmar_contraseña = forms.CharField(widget=forms.PasswordInput(), label='Confirmar Contraseña')

    class Meta:
        model = Trabajador
        fields = ['perfil','nombre', 'paterno', 'materno', 'sexo', 'rut', 'fecha_nacimiento', 'telefono', 'correo', 'contraseña', 'confirmar_contraseña', 'foto']
        widgets = {
            'fecha_nacimiento': forms.SelectDateWidget(years=range(1900, 2024)),
            'contraseña': forms.PasswordInput(),
        }

    def clean_contraseña(self):
        contraseña = self.cleaned_data.get('contraseña')

        if len(contraseña) < 8 or not re.search(r'[A-Z]', contraseña) or not re.search(r'[!@#$%^&*(),.?":{}|<>]', contraseña):
            raise forms.ValidationError('La contraseña debe tener al menos 8 caracteres, una mayúscula y un símbolo.')

        return contraseña

    def clean(self):
        cleaned_data = super().clean()
        contraseña = cleaned_data.get('contraseña')
        confirmar_contraseña = cleaned_data.get('confirmar_contraseña')

        if contraseña and confirmar_contraseña and contraseña != confirmar_contraseña:
            self.add_error('confirmar_contraseña', 'Las contraseñas no coinciden.')

        return cleaned_data

    def clean_fecha_nacimiento(self):
        fecha_nacimiento = self.cleaned_data.get('fecha_nacimiento')

        if fecha_nacimiento and fecha_nacimiento > date.today():
            raise ValidationError('La fecha de nacimiento no puede ser en el futuro.')

        return fecha_nacimiento

    def clean_correo(self):
        correo = self.cleaned_data.get('correo')

        try:
            validate_email(correo)
        except ValidationError:
            raise ValidationError('Ingrese una dirección de correo electrónico válida.')

        return correo
    
    def clean_rut(self):
        rut = self.cleaned_data.get('rut')

        # Verifica si el RUT tiene el formato correcto
        if not rut or not self.validate_rut_format(rut):
            raise ValidationError('Ingrese un RUT válido.')


        return rut

    def validate_rut_format(self, rut):
        parts = rut.split('-')

    # Asegura de que haya dos partes (cuerpo y dígito verificador)
        if len(parts) != 2:
            return False

        body, verifier = parts

    # Asegura de que el cuerpo tenga al menos 9 caracteres
        if len(body) < 7:
            return False

    # Verifica que el cuerpo y el dígito verificador tengan el formato correcto
        if not body.isdigit() or (not verifier.isdigit() and verifier.upper() != 'K'):
            return False

        return True


class TrabajadorEditForm(forms.ModelForm):
    class Meta:
        model = Trabajador
        fields = ['nombre', 'paterno', 'materno', 'sexo', 'rut', 'fecha_nacimiento', 'telefono', 'correo', 'contraseña', 'foto']
        widgets = {
            'fecha_nacimiento': forms.DateInput(),
        }

    perfil = forms.ModelChoiceField(queryset=PerfilTrabajador.objects.all(), required=False)

    def clean_contraseña(self):
        contraseña = self.cleaned_data.get('contraseña')

        if len(contraseña) < 8:
            raise ValidationError('La contraseña debe tener al menos 8 caracteres.')
        
        if not re.search(r'[A-Z]', contraseña) or not re.search(r'[!@#$%^&*(),.?":{}|<>]', contraseña):
            raise forms.ValidationError('La contraseña debe contener al menos una mayúscula y un símbolo.')

        return contraseña

    

    def clean_fecha_nacimiento(self):
        fecha_nacimiento = self.cleaned_data.get('fecha_nacimiento')

        if fecha_nacimiento and fecha_nacimiento > date.today():
            raise ValidationError('La fecha de nacimiento no puede ser en el futuro.')

        return fecha_nacimiento

    def clean_correo(self):
        correo = self.cleaned_data.get('correo')

        try:
            validate_email(correo)
        except ValidationError:
            raise ValidationError('Ingrese una dirección de correo electrónico válida.')

        return correo

    
    def clean_rut(self):
        rut = self.cleaned_data.get('rut')

        # Verifica si el RUT tiene el formato correcto
        if not rut or not self.validate_rut_format(rut):
            raise ValidationError('Ingrese un RUT válido.')


        return rut

    def validate_rut_format(self, rut):
        parts = rut.split('-')

    # Asegura de que haya dos partes (cuerpo y dígito verificador)
        if len(parts) != 2:
            return False

        body, verifier = parts

    # Asegura que el cuerpo tenga al menos 9 caracteres
        if len(body) < 7:
            return False

    # Verifica que el cuerpo y el dígito verificador tengan el formato correcto
        if not body.isdigit() or (not verifier.isdigit() and verifier.upper() != 'K'):
            return False

        return True
    
    

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





class DetalleCompraForm(forms.ModelForm):
    class Meta:
        model = DetalleCompra
        fields = ['producto', 'cantidad', 'precio_unitario']

    producto = forms.ModelChoiceField(queryset=Producto.objects.all())

class CompraProveedorForm(forms.ModelForm):
    class Meta:
        model = CompraProveedor
        fields = ['numero_factura', 'proveedor', 'rut_proveedor', 'correo_proveedor', 'fecha_compra']
        widgets = {
            'fecha_compra': forms.SelectDateWidget(years=range(2023, 2051)),
            'numero_factura': forms.TextInput(attrs={'type': 'number', 'min': 0, 'autocomplete': 'off'}),

        }
    
    def clean_numero_factura(self):
        numero_factura = self.cleaned_data.get('numero_factura')

        # Verificar si el número de factura ya existe en la base de datos
        if CompraProveedor.objects.filter(numero_factura=numero_factura).exists():
            raise forms.ValidationError("Este número de factura ya está registrado. Por favor, ingresa uno diferente.")

        # Validar si el número de factura contiene solo dígitos
        if not numero_factura.isdigit():
            raise forms.ValidationError("El número de factura debe contener solo números.")

        return numero_factura
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