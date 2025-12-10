from django.db import transaction
from rest_framework import serializers
from .models import Categoria, Proveedor, Producto, MovimientoStock


# ----------------------
# CATEGORIAS
# ----------------------
class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'


# ----------------------
# PROVEEDORES
# ----------------------
class ProveedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proveedor
        fields = '__all__'


# ----------------------
# PRODUCTOS
# ----------------------
class ProductoSerializer(serializers.ModelSerializer):
    categoria_nombre = serializers.ReadOnlyField(source='categoria.nombre')
    proveedor_nombre = serializers.ReadOnlyField(source='proveedor.nombre')

    class Meta:
        model = Producto
        fields = '__all__'

    def validate_stock_actual(self, value):
        if value < 0:
            raise serializers.ValidationError('El stock actual no puede ser negativo.')
        return value

    def validate_stock_minimo(self, value):
        if value < 0:
            raise serializers.ValidationError('El stock mínimo no puede ser negativo.')
        return value


# ----------------------
# MOVIMIENTOS DE STOCK
# ----------------------
class MovimientoStockSerializer(serializers.ModelSerializer):
    producto_nombre = serializers.ReadOnlyField(source='producto.nombre')

    class Meta:
        model = MovimientoStock
        fields = '__all__'
        read_only_fields = ['creado_en']

    # VALIDACIÓN GENERAL
    def validate(self, attrs):
        producto = attrs.get('producto')
        tipo = attrs.get('tipo')
        cantidad = attrs.get('cantidad')

        if cantidad <= 0:
            raise serializers.ValidationError({'cantidad': 'Debe ser mayor a cero.'})

        # VALIDACIÓN PARA EVITAR STOCK NEGATIVO
        if tipo == MovimientoStock.TIPO_SALIDA:
            if producto.stock_actual - cantidad < 0:
                raise serializers.ValidationError(
                    {'cantidad': 'Este movimiento dejaría el stock en negativo.'}
                )
        return attrs

    # CREACIÓN DEL MOVIMIENTO + ACTUALIZACIÓN DE STOCK
    @transaction.atomic
    def create(self, validated_data):
        producto = validated_data['producto']
        tipo = validated_data['tipo']
        cantidad = validated_data['cantidad']

        if tipo == MovimientoStock.TIPO_SALIDA:
            nuevo_stock = producto.stock_actual - cantidad
            if nuevo_stock < 0:
                raise serializers.ValidationError(
                    {'cantidad': 'El movimiento generaría stock negativo.'}
                )
            producto.stock_actual = nuevo_stock
        else:
            producto.stock_actual += cantidad

        producto.save()

        movimiento = MovimientoStock.objects.create(**validated_data)
        return movimiento
