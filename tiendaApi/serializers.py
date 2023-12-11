from rest_framework import serializers
from tiendaApp.models import Producto

class ProductoSerializar(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__'
