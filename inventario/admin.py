from django.contrib import admin
from .models import Categoria, Proveedor, Producto, MovimientoStock


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'descripcion', 'creado_en')
    search_fields = ('nombre',)


@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'email', 'telefono', 'activo')
    search_fields = ('nombre', 'email')
    list_filter = ('activo',)


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'sku', 'nombre', 'categoria', 'proveedor',
        'precio', 'stock_actual', 'stock_minimo', 'activo'
    )
    search_fields = ('nombre', 'sku')
    list_filter = ('categoria', 'proveedor', 'activo')


@admin.register(MovimientoStock)
class MovimientoStockAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'producto', 'tipo', 'cantidad', 'creado_en'
    )
    list_filter = ('tipo', 'producto')
    search_fields = ('producto__nombre', 'motivo')
