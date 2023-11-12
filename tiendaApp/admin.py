from django.contrib import admin

# Register your models here.
from tiendaApp.models import Categoria, Subcategoria, Producto

class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'creado']
    
class SubcategoriaAdmin(admin.ModelAdmin):
    list_display = ['categoria', 'nombre', 'creado']
    
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'marca', 'precio',
                    'cantidad', 'categoria', 'subcategoria',
                    'primerJuguete', 'descripcion', 'creado']
    
admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Subcategoria, SubcategoriaAdmin)
admin.site.register(Producto, ProductoAdmin)