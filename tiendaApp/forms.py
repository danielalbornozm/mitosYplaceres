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
    descripcion = forms.CharField(widget=forms.TextInput(
        attrs={'class':'form-control', 'placeholder': 'Ingrese descripción del producto'}))
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